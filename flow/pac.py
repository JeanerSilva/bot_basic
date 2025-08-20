import siop_utils as sb
import os
from pathlib import Path
from .objetivo_especifico import objetivo_especifico


class pac_lote:
    def __init__(self, exercicio: str, pasta: str, data_referencia: str, reiniciar_driver_entre_arquivos: bool = True):
        if not exercicio or not str(exercicio).strip():
            raise ValueError("❌ Parâmetro 'exercicio' é obrigatório e não pode estar vazio.")
        if not pasta or not str(pasta).strip():
            raise ValueError("❌ Parâmetro 'pasta' é obrigatório e não pode estar vazio.")
        if not data_referencia or not str(data_referencia).strip():
            raise ValueError("❌ Parâmetro 'data_referencia' é obrigatório e não pode estar vazio.")

        self.exercicio = exercicio
        self.pasta = pasta
        self.data_referencia = data_referencia
        self.reiniciar_driver_entre_arquivos = reiniciar_driver_entre_arquivos

    def atualizar(self):
        sb.define_exercicio(self.exercicio)

        os.makedirs("prints", exist_ok=True)

        path = Path(self.pasta)
        arquivos = sorted(path.glob("*.xlsx"))
        if not arquivos:
            print("⚠️ Nenhum arquivo encontrado.")
            return

        for arq in arquivos:
            if arq.name.startswith("enviado."):
                continue

            num = sb.extrai_numero_pac(arq.name)
            if num is None:
                continue

            objetivo = sb.monta_objetivo(num)
            arquivo = str(path / arq.name)

            objetivo_especifico(objetivo)\
                .acessa()\
                .lista()\
                .seleciona_objetivo_listado()\
                .apaga_arquivo_pac()\
                .adiciona_arquivo_pac(
                    f"OE {objetivo}: Ações do Novo PAC (Data de referência: {self.data_referencia}).",
                    arquivo,
                    objetivo,
                    self.exercicio,
                )

            print(f"✅ OE {objetivo} atualizado com sucesso.")

            novo_nome = arq.with_name(f"enviado.{arq.name}")
            try:
                arq.rename(novo_nome)
                print(f"✅ Arquivo renomeado: {novo_nome}")
            except Exception as e:
                print(f"⚠️ Não consegui renomear {arq.name}: {e}")

            if self.reiniciar_driver_entre_arquivos:
                sb.encerra()
                sb.finaliza_navegador()
                sb.iniciar_driver()

        return self


def atualizar_pac_em_lote(exercicio: str, pasta: str, data_referencia: str, reiniciar_driver_entre_arquivos: bool = True):
    return pac_lote(exercicio, pasta, data_referencia, reiniciar_driver_entre_arquivos).atualizar()


