import os
from datetime import datetime
from fpdf import FPDF
from PIL import Image

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Relatório Meteorológico Completo', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Estação: Florianópolis/SC (A806) | Período: 2010-2025", 0, 1, 'C')
        self.cell(0, 10, f"Data do relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_image_with_title(self, image_path, title, description=None):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        
        if description:
            self.set_font('Arial', '', 12)
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
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f"Erro ao carregar imagem: {str(e)}", 0, 1)
        
        self.ln(10)

def generate_report(output_dir="imagens_resultados", report_file="relatorio_meteorologico.pdf", author_name="Eduardo Hansen"):
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
    pdf.set_author(author_name)  # Aqui definimos o autor com seu nome
    
    # Capa personalizada
    pdf.add_page()
    pdf.set_font('Arial', 'B', 22)
    pdf.cell(0, 40, 'RELATÓRIO METEOROLÓGICO', 0, 1, 'C')
    pdf.ln(20)
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Estação: Florianópolis/SC (A806)', 0, 1, 'C')
    pdf.cell(0, 10, 'Período: 2010-2025', 0, 1, 'C')
    pdf.ln(20)
    
    pdf.set_font('Arial', '', 14)
    pdf.multi_cell(0, 10, "Este relatório contém análises completas dos dados meteorológicos coletados, incluindo temperaturas, precipitação, pressão atmosférica, umidade, vento e radiação solar.")
    pdf.ln(15)
    
    # Adicionando seu nome na capa
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Gerado por: {author_name}", 0, 1, 'C')
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
    
    # Restante do código permanece igual...
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Índice', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', '', 12)
    for i, img_file in enumerate(image_files, 1):
        title, _ = image_descriptions.get(img_file, (img_file.replace('.png', '').replace('_', ' ').title(), ''))
        pdf.cell(0, 10, f"{i}. {title}", 0, 1)
    
    for img_file in image_files:
        img_path = os.path.join(output_dir, img_file)
        title, description = image_descriptions.get(img_file, (img_file.replace('.png', '').replace('_', ' ').title(), ''))
        pdf.add_image_with_title(img_path, title, description)
    
    try:
        pdf.output(report_file)
        print(f"\n✅ Relatório gerado com sucesso: {os.path.abspath(report_file)}")
        print(f"👤 Autor: {author_name}")
    except Exception as e:
        print(f"\n❌ Erro ao salvar relatório: {str(e)}")

if __name__ == "__main__":
    # Substitua "Seu Nome" pelo seu nome real
    generate_report(author_name="Eduardo Hansen")