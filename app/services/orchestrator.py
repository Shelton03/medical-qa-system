from typing import Union
from app.models.domain import Session, Message
from app.api.responses import AskResponseData, AnswerResponseData
from app.db.repositories import SessionRepository, MessageRepository
from app.services.input_processor import InputProcessor
from app.services.assessment import AssessmentService
from app.services.decision_engine import DecisionEngine
from app.services.question_gen import QuestionGenerator
from app.services.answer_gen import AnswerGenerator
from app.core.logger import logger

class Orchestrator:
    def __init__(self, session_repo: SessionRepository, message_repo: MessageRepository):
        self.session_repo = session_repo
        self.message_repo = message_repo
        
        # Initialize sub-services
        self.input_processor = InputProcessor()
        self.assessment_service = AssessmentService()
        self.decision_engine = DecisionEngine()
        self.question_gen = QuestionGenerator()
        self.answer_gen = AnswerGenerator()

    async def handle_query(self, session_id: str | None, user_text: str) -> Union[AskResponseData, AnswerResponseData]:
        logger.info(f"--- Handling Query for Session: {session_id or 'NEW'} ---")
        # 1. Load or Create Session
        if session_id:
            session = await self.session_repo.get_session(session_id)
            if not session:
                session = Session(session_id=session_id)
                await self.session_repo.create_session(session)
        else:
            session = Session()
            await self.session_repo.create_session(session)
        logger.info(f"Loaded session: {session.session_id}")

        # 2. Persist User Message
        user_msg = Message(
            session_id=session.session_id,
            role="user",
            content=user_text,
            message_type="initial" if not session.assessment_done else "question"
        )
        await self.message_repo.add_message(user_msg)

        # 3. Process Input (Structured data extraction from current message)
        logger.info("Step 1: Processing user input for entities...")
        processed_data = await self.input_processor.process(user_text)
        logger.debug(f"Processed input: {processed_data}")
        # Note: We are not applying this directly to the session anymore. 
        # The decision engine will synthesize the state from the full context.

        # 4. Initial Assessment (if needed)
        if not session.assessment_done:
            logger.info("Step 2: Performing initial medical assessment...")
            session = await self.assessment_service.perform_initial_assessment(session, user_text, processed_data)
            logger.info(f"Assessment complete. Risk flags: {session.risk_flags}")
        
        # 5. Build History Context
        history_msgs = await self.message_repo.get_session_history(session.session_id)
        history_text = "\n".join([f"{m.role.upper()}: {m.content}" for m in history_msgs])

        # 6. Decision Engine & State Synthesis
        logger.info("Step 3: Running Decision Engine and State Synthesizer...")
        decision_data = await self.decision_engine.evaluate(session, history_text)
        decision = decision_data["decision"]
        logger.info(f"Engine Decision: {decision} | Confidence: {session.confidence:.2f}")

        # 7. State Synchronization
        logger.info("Step 4: Synchronizing session state...")
        state_update = decision_data.get("state_update", {})
        
        # Merge and de-duplicate lists
        session.key_symptoms = list(set(session.key_symptoms + state_update.get("key_symptoms", [])))
        session.risk_flags = list(set(session.risk_flags + state_update.get("risk_flags", [])))
        
        # Overwrite missing_info as it's meant to be a current snapshot
        session.missing_info = state_update.get("missing_info", [])
        session.gaps_remaining = len(session.missing_info)
        
        logger.debug(f"Synchronized state. Gaps: {session.gaps_remaining}, Symptoms: {session.key_symptoms}")
        
        # 8. Generate Response based on Decision
        response_data = None
        assistant_msg_content = ""
        msg_type = ""

        if decision == "ASK":
            logger.info("Step 5: Generating next clinical question...")
            question_text = await self.question_gen.generate_next_question(session, history_text)
            assistant_msg_content = question_text
            msg_type = "question"
            
            response_data = AskResponseData(
                session_id=session.session_id,
                assessment_done=session.assessment_done,
                confidence=session.confidence,
                content=question_text
            )
        
        else: # ANSWER
            logger.info("Step 5: Generating final medical answer...")
            ans_data = await self.answer_gen.generate_answer(session, history_text)
            assistant_msg_content = ans_data.get("content", "")
            msg_type = "answer"
            
            response_data = AnswerResponseData(
                session_id=session.session_id,
                assessment_done=session.assessment_done,
                confidence=session.confidence,
                content=ans_data.get("content", ""),
                explanation=ans_data.get("explanation", ""),
                disclaimer=ans_data.get("disclaimer", ""),
                confidence_level=ans_data.get("confidence_level", "low")
            )

        # 9. Persist Assistant Response
        bot_msg = Message(
            session_id=session.session_id,
            role="assistant",
            content=assistant_msg_content,
            message_type=msg_type
        )
        await self.message_repo.add_message(bot_msg)

        # 10. Persist Final Session State
        await self.session_repo.update_session(session)

        return response_data
