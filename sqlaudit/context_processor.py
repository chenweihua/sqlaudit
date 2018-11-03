# -*- coding: utf-8 -*-
#


def jumpserver_processor(request):
    context = {}

    # Setting default pk
    context.update(
        {'DEFAULT_PK': 999999999}
    )
    return context



