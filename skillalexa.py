import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler para o lançamento da Skill."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Agora você pode controlar seu computador."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ComputadorRemotoIntentHandler(AbstractRequestHandler):
    """Handler para o controle remoto do computador."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ComputadorRemotoIntent")(handler_input)

    def handle(self, handler_input):
        site = ask_utils.get_slot_value(handler_input, "acessarsite")
        app = ask_utils.get_slot_value(handler_input, "acessarapp")
        desligar = ask_utils.get_slot_value(handler_input, "desligarcomputador")

        if site:
            try:
                speak_output = f"Acessando o site {site} no seu computador."
                response = requests.get(f"https://----------------/navegarInternet/{site}")
                response.raise_for_status()
            except requests.exceptions.RequestException:
                speak_output = f"Erro ao acessar o site {site} no seu computador."

        elif app:
            try:
                speak_output = f"Acessando o app {app} no seu computador."
                response = requests.get(f"https://----------------//abrirAplicativo/{app}")
                response.raise_for_status()
            except requests.exceptions.RequestException:
                speak_output = f"Erro ao acessar o aplicativo {app} no seu computador."

        elif desligar:
            try:
                speak_output = "Desligando o seu computador."
                response = requests.get("https://----------------//desligarComputador")
                response.raise_for_status()
            except requests.exceptions.RequestException:
                speak_output = "Erro ao desligar seu computador."

        else:
            speak_output = "Desculpe, não entendi o que você quer fazer. Pode repetir?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler para o pedido de ajuda."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Você pode me dizer para acessar um site, abrir um app ou desligar o computador. Como posso ajudar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler para Cancelar ou Parar."""
    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
            ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        )

    def handle(self, handler_input):
        speak_output = "Até logo!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler para respostas inesperadas."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("FallbackIntentHandler ativado")
        speech = "Hmm, não tenho certeza. Você pode pedir ajuda ou tentar outro comando."
        reprompt = "Não entendi. Em que posso te ajudar?"

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler para o fim da sessão."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """Handler de teste que reflete o nome do intent disparado."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = f"Você acabou de acionar o intent {intent_name}."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Handler genérico para capturar erros e exceções."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Desculpe, tive um problema ao tentar fazer o que você pediu. Tente novamente, por favor."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Registro dos handlers na skill
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ComputadorRemotoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# Lambda handler