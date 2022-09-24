from wpo_logic.models import CodigosPostales


def get_all_codigos_postales(key_word):
    return CodigosPostales.objects.filter(codigo_postal__exact=key_word)
