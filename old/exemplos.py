preenche_seletor_por_id(driver, wait, "Programa",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoPrograma",
        "1144 - Agropecuária Sustentável"
    )
    preenche_seletor_por_id(driver, wait, "Órgão",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoOrgao",
        "22000 - Ministério da Agricultura e Pecuária"
    )
    preenche_seletor_por_id(driver, wait, "Origem",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoTipoInclusao", "PPA"
    )
    preenche_seletor_por_id(driver, wait, "Momento",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoMomento", "Base de Partida"
    )
    preenche_seletor_por_id(driver, wait, "Alterado",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoAlterado", "Alterado"
    )
    preenche_seletor_por_id(driver, wait, "Excluído",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoExcluido", "Não Excluído"
    )
    preenche_seletor_por_id(driver, wait, "Novo",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoNovo", "Novo"
    )
    preenche_seletor_por_id(driver, wait, "Validado",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoValidado", "Validado"
    )