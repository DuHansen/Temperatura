import os
from datetime import datetime
from fpdf import FPDF, XPos, YPos
from PIL import Image

class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", 'B', 16)
        self.cell(0, 10, 'Relatório Meteorológico Completo', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font("helvetica", '', 12)
        self.cell(0, 10, f"Estação: Florianópolis/SC (A806) | Período: 2010-2025", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(0, 10, f"Data do relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def add_image_with_title(self, image_path, title, description=None):
        self.add_page()
        self.set_font("helvetica", 'B', 14)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        
        if description:
            self.set_font("helvetica", '', 12)
            self.multi_cell(0, 8, description)
            self.ln(5)
        
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                aspect = w / h
                
                max_width = 180
                new_width = min(w, max_width)
                new_height = new_width / aspect
                
                max_height = 250
                if new_height > max_height:
                    new_height = max_height
                    new_width = new_height * aspect
                
                self.image(image_path, x=(210 - new_width)/2, y=None, w=new_width, h=new_height)
        except Exception as e:
            self.set_font("helvetica", 'I', 10)
            self.cell(0, 10, f"Erro ao carregar imagem: {str(e)}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.ln(10)

def generate_report(output_dir="imagens_resultados", report_file="relatorio_meteorologico_completo.pdf", author_name="Eduardo Hansen"):
    if not os.path.exists(output_dir):
        print(f"❌ Diretório '{output_dir}' não encontrado.")
        return
    
    image_files = sorted([f for f in os.listdir(output_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print("❌ Nenhuma imagem encontrada para gerar o relatório.")
        return
    
    image_descriptions = {
        'tabela_temperaturas.png': ('Tabela de Temperaturas por Ano', 
                                   'Estatísticas anuais de temperaturas (média, máxima e mínima) no período analisado.'),
        'tendencia_temperatura.png': ('Tendência de Temperatura Anual', 
                                     'Evolução das temperaturas medianas, máximas e mínimas ao longo dos anos.'),
        'distribuicao_temperatura.png': ('Distribuição de Temperaturas por Ano', 
                                        'Boxplot mostrando a variação das temperaturas médias em cada ano.'),
        'distribuicao_precipitacao.png': ('Distribuição de Precipitação', 
                                         'Histograma da precipitação total acumulada durante todo o período.'),
        'temp_vs_umidade.png': ('Relação entre Temperatura e Umidade', 
                               'Gráfico de dispersão mostrando a correlação entre temperatura do ar e umidade relativa.'),
        'distribuicao_pressao.png': ('Distribuição de Pressão Atmosférica', 
                                    'Histograma dos valores de pressão atmosférica registrados na estação.'),
        'distribuicao_vento.png': ('Distribuição de Velocidade do Vento', 
                                  'Histograma da velocidade do vento registrada durante o período.'),
        'distribuicao_radiacao.png': ('Distribuição de Radiação Global', 
                                     'Histograma dos valores de radiação solar global incidente.')
    }

    pdf = PDFReport()
    pdf.set_title("Relatório Meteorológico")
    pdf.set_author(author_name)
    
    # Capa personalizada
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 22)
    pdf.cell(0, 40, 'RELATÓRIO METEOROLÓGICO', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(20)
    
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, 'Estação: Florianópolis/SC (A806)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 10, 'Período: 2010-2025', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(20)
    
    pdf.set_font("helvetica", '', 14)
    pdf.multi_cell(0, 10, "Este relatório contém análises completas dos dados meteorológicos coletados, incluindo temperaturas, precipitação, pressão atmosférica, umidade, vento e radiação solar.")
    pdf.ln(15)
    
    # Adicionando nome do autor na capa
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, f"Gerado por: {author_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    # Sumário
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, 'Sumário', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "Esta pesquisa tem a finalidade de conduzir um reconhecimento inicial das informações do tempo reunidas pela estação de Florianópolis/SC (A806) entre 2010 e 2025. Adotando métodos de ciência de dados, as características do tempo, como temperatura, chuva, pressão do ar, umidade, vento e luz do sol, foram avaliadas, visando identificar padrões, caminhos e possíveis ligações. A avaliação criou representações visuais relevantes, como gráficos de dispersão, diagramas de caixa e histogramas, oferecendo percepções importantes sobre o clima da área.")
    pdf.ln(10)
    
    # Introdução
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '1. Introdução', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(5)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "A avaliação de dados do tempo é uma ferramenta essencial para entender as mudanças no clima e seu efeito em diversos setores, como saúde, agricultura e planejamento das cidades. Este estudo emprega dados do tempo da estação Florianópolis/SC (A806) obtidos de 2010 a 2025, buscando explorar as mudanças de temperatura, chuva e outras características do ar.")
    pdf.ln(10)
    
    # Metodologia
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '2. Metodologia', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(5)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "2.1 Coleta e Apresentação das Informações\n\nAs informações utilizadas neste estudo foram retiradas da estação meteorológica de Florianópolis/SC, abrangendo o período de 2010 a 2025. As características analisadas incluem:\n\n- Temperatura: Média, máxima e mínima.\n- Chuva: Total acumulado ao longo do período.\n- Pressão do Ar, Umidade, Velocidade do Vento e Luz do Sol.\n\nA coleta foi feita em formato CSV e uma limpeza das informações foi realizada, retirando valores ausentes e extremos, além de ajustar algumas características para análise.")
    pdf.ln(10)
    
    pdf.multi_cell(190, 10, "2.2 Tratamento das Informações\n\nAs informações passaram por diversas etapas de tratamento, incluindo a retirada de valores ausentes e a inclusão de informações faltantes. Para auxiliar na análise, as características de temperatura e umidade foram ajustadas, e métodos estatísticos foram utilizados para a detecção de valores extremos.")
    pdf.ln(10)
    
    pdf.multi_cell(190, 10, "2.3 Análise Preliminar\n\nForam aplicadas técnicas de estatísticas descritivas (média, mediana, desvio padrão) para compreender o comportamento das características. Além disso, gráficos como histogramas, diagramas de caixa e gráficos de dispersão foram gerados para identificar caminhos e ligações entre as características, como a relação entre temperatura e umidade.")
    pdf.ln(10)
    
    # Resultados
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '3. Resultados', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(5)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "3.1 Temperatura\n\nA análise revelou uma tendência de elevação das temperaturas máximas ao longo dos anos, principalmente nos anos recentes. A temperatura média também apresentou um pequeno aumento, refletindo a tendência global de aquecimento.")
    pdf.ln(10)
    
    pdf.multi_cell(190, 10, "3.2 Chuva\n\nA chuva apresentou variações sazonais, com picos durante o verão. A distribuição da chuva não apresentou caminhos claros, mas os eventos de chuva extrema ocorreram com maior frequência nos últimos anos.")
    pdf.ln(10)
    
    pdf.multi_cell(190, 10, "3.3 Ligação entre Temperatura e Umidade\n\nVerificou-se que quando a temperatura subia, o ar ficava menos úmido, mostrando uma ligação entre esses dois fatores.")
    pdf.ln(10)
    
    pdf.multi_cell(190, 10, "3.4 Luz do Sol e Correntes de Ar\n\nA quantidade de luz solar mudou de acordo com a época do ano, sendo maior nos meses de verão. A força do vento não variou muito ao longo dos anos, mantendo-se estável.")
    pdf.ln(10)
    
    # Análise
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '4. Análise', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(5)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "Os dados coletados apontam para uma influência das alterações climáticas globais em Florianópolis, com um aumento gradual das temperaturas e a ocorrência mais intensa de eventos climáticos incomuns, como chuvas torrenciais. A relação entre temperatura e umidade pode ajudar a entender como as pessoas se sentem em relação ao calor, principalmente no verão.")
    pdf.ln(10)
    
    # Considerações Finais
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '5. Considerações Finais', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(5)
    pdf.set_font("helvetica", '', 12)
    pdf.multi_cell(190, 10, "Esta pesquisa fornece um panorama completo das mudanças climáticas em Florianópolis no período de 2010 a 2025. Ao analisarmos os dados do tempo, notamos tendências importantes, como o aumento das temperaturas e a ligação entre temperatura e umidade. Em breve, outras pesquisas poderão analisar as previsões para os próximos anos, usando modelos climáticos preditivos.")
    pdf.ln(10)
    
    # Adicionar imagens com descrições
    for image_file in image_files:
        title, description = image_descriptions.get(image_file, (image_file, None))
        image_path = os.path.join(output_dir, image_file)
        pdf.add_image_with_title(image_path, title, description)
    
    # Referências
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, '6. Referências', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)

    pdf.set_font("helvetica", '', 12)
    references = [
        "1. Silva, F. R., et al. Mudanças Climáticas no Brasil: Uma Análise das Tendências de Temperatura e Precipitação. Revista Brasileira de Meteorologia, 2020.",
        "2. Medeiros, M. S., et al. Análise de Dados Climáticos e suas Implicações nas Condições Ambientais e Agrícolas. Journal of Climate, 2021.",
        "3. Instituto Nacional de Meteorologia (INMET). Estação Meteorológica Florianópolis/SC (A806). Disponível em: http://inmet.gov.br",
        "4. Agência Nacional de Águas (ANA). Relatório de Precipitação no Brasil. 2022."
    ]

    for ref in references:
        pdf.multi_cell(190, 10, ref)
        pdf.ln(5)
    
    try:
        pdf.output(report_file)
        print(f"\n✅ Relatório gerado com sucesso: {report_file}")
    except Exception as e:
        print(f"\n❌ Erro ao salvar relatório: {str(e)}")

if __name__ == "__main__":
    generate_report(author_name="Eduardo Hansen")