from django.shortcuts import render
from socios.models import Socio, Mensalidade
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph, Table, TableStyle, Spacer, Frame, PageTemplate, BaseDocTemplate, Image
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
#from django.db.models import Count, Q
from collections import Counter
from django.core.serializers.json import DjangoJSONEncoder
import json




CAMINHO_LOGO = 'C:/Gilmar/Django2023/nadinmarreis/templates/static/img/bandeira.jpeg' 

#-- função ===============================================================================
def add_cabecalho_rodape(canvas, doc):
    # Salva o estado do canvas para não afetar o restante do documento
    canvas.saveState()
    # Adiciona o cabeçalho
    header_text = "                 S.E.R. Nadin Marreis"
    #styles = getSampleStyleSheet()
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawString(inch, doc.pagesize[1] - inch, header_text)
    # Adiciona o logo no cabeçalho (substitua 'logo.png' pelo caminho da sua imagem)
    logo_path = CAMINHO_LOGO
    logo = Image(logo_path, width=0.9*inch, height=0.6*inch)
    logo.drawOn(canvas, inch, doc.pagesize[1] - 1.25*inch)
    # Adiciona o rodapé
    footer_text = "Página %d" % doc.page
    canvas.setFont("Helvetica", 10)
    canvas.drawString(inch, 0.75 * inch, footer_text)
    # Restaura o estado do canvas
    canvas.restoreState()


#-- função ===============================================================================
def totalizar_mensalidades_por_ano():
    anos = Mensalidade.objects.values_list('ano', flat=True).distinct()
    anos = anos.order_by('ano')
    resultado = []
    for ano in anos:
        mensalidades = Mensalidade.objects.filter(ano=ano)
        total_true = 0
        total_false = 0
        for mensalidade in mensalidades:
            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            for mes in meses:
                if getattr(mensalidade, mes):
                    total_true += 1
                else:
                    total_false += 1
        resultado.append({
            'ano': ano,
            'total_true': total_true,
            'total_false': total_false
            })
    return resultado

#-- views ===============================================================================

def relatorio_socios_pdf(request):
    # Agrupa os sócios por tipo
    socios_por_tipo = {}
    for tipo in Socio.TIPOS_SOCIO:
        socios = Socio.objects.filter(tipo_socio=tipo[0]).order_by('nome')
        if socios:
            socios_por_tipo[tipo[1]] = socios  # Usa o nome do tipo como chave
    # Cria o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_socios.pdf"'
    # Configura o documento PDF com BaseDocTemplate
    doc = BaseDocTemplate(response, pagesize=letter)
    doc.setTitle("Relatorio_socios")  # Define o título do PDF
    frame = Frame(inch, inch, doc.width, doc.height - 2 * inch, id='normal')  # Define a área útil da página
    template = PageTemplate(id='test', frames=frame, onPage=add_cabecalho_rodape)  # Adiciona o cabeçalho e rodapé
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    elements = []
    # Adiciona um título ao PDF
    # elements.append(Paragraph("Relatório de Sócios por Tipo", styles['Title']))

    # Cria uma tabela para cada tipo de sócio
    for tipo, socios in socios_por_tipo.items():
        elements.append(Paragraph(f"Tipo de Sócio: {tipo}", styles['Heading2']))

        # Prepara os dados da tabela
        data = [['Nome', 'Tipo de Sócio', 'Telefone', 'Cidade']]
        for socio in socios:
            data.append([socio.nome,  f"{socio.get_tipo_socio_display()} - Titulo({socio.num_titulo})" or '', socio.telefone or '', socio.cidade or ''])

        # Cria a tabela
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            # Alinha o nome à esquerda (primeira coluna)
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Alinha o conteúdo da coluna 0 (nome) à esquerda
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),  # Alinha o conteúdo da coluna 0 (cidade) à esquerda
        ]))

        elements.append(table)
        elements.append(Paragraph(" ", styles['Normal']))  # Espaço entre tabelas

    # Gera o PDF
    doc.build(elements)
    return response


#-- views ===============================================================================
def gerar_relatorio_socio_pdf(request):
    # Cria um objeto HttpResponse com o cabeçalho de PDF apropriado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_socios.pdf"'
    # Cria o objeto PDF, usando o objeto response como seu "arquivo"
    p = canvas.Canvas(response, pagesize=letter)
    # Define o título do relatório
    p.drawString(100, 750, "Relatório de Sócios")
    # Define a posição inicial para o texto
    y = 700
    # Obtém todos os sócios do banco de dados
    socios = Socio.objects.all().order_by('nome')
    # Itera sobre os sócios e adiciona as informações ao PDF
    for socio in socios:
        p.drawString(100, y, f"Nome: {socio.nome}")
        p.drawString(100, y - 20, f"Email: {socio.email}")
        p.drawString(100, y - 40, f"Telefone: {socio.telefone}")
        p.drawString(100, y - 60, f"Data de Nascimento: {socio.data_nascimento}")
        p.drawString(100, y - 80, f"Data de Admissão: {socio.data_admisao}")
        p.drawString(100, y - 100, f"Tipo de Sócio: {socio.get_tipo_socio_display()} - Titulo({socio.num_titulo})")
        p.drawString(100, y - 120, f"Ativo: {'Sim' if socio.ativo else 'Não'}")
        p.drawString(100, y - 140, f"CPF: {socio.cpf}")
        p.drawString(100, y - 160, f"RG: {socio.rg}")
        p.drawString(100, y - 180, f"Endereço: {socio.endereco}")
        p.drawString(100, y - 200, f"Cidade/Estado: {socio.cidade} - CEP: {socio.cep}")
        p.drawString(100, y - 220, f"Esporte Preferido: {socio.esporte}")
        p.drawString(100, y - 240, f"Observações: {socio.observacao}")
        # Adiciona uma linha separadora
        p.line(100, y - 260, 500, y - 260)
        # Move para a próxima linha
        y -= 280
        # Verifica se a página está cheia e adiciona uma nova página
        if y < 100:
            p.showPage()
            y = 750

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response

#-- views ===============================================================================
def relatorio_socios_mensalidades_pdf(request):
    # Busca todos os sócios e suas mensalidades
    socios = Socio.objects.all().order_by('nome')
    mensalidades = Mensalidade.objects.all().order_by('ano')

    # Agrupa as mensalidades por sócio
    socios_com_mensalidades = {}
    for socio in socios:
        mensalidades_socio = mensalidades.filter(socio=socio)
        if mensalidades_socio:
            socios_com_mensalidades[socio] = mensalidades_socio

    # Cria o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_mensalidades.pdf"'
    # Configura o documento PDF com BaseDocTemplate
    doc = BaseDocTemplate(response, pagesize=letter)
    doc.setTitle("Relatorio_mensalidades")  # Define o título do PDF
    frame = Frame(inch, inch, doc.width, doc.height - 2 * inch, id='normal')  # Define a área útil da página
    template = PageTemplate(id='test', frames=frame, onPage=add_cabecalho_rodape)  # Adiciona o cabeçalho e rodapé
    doc.addPageTemplates([template])
    styles = getSampleStyleSheet()
    elements = []

    # Adiciona um título ao PDF
    elements.append(Paragraph("Relatório de Sócios e Mensalidades", styles['Title']))
    elements.append(Spacer(1, 6))  # Adiciona um espaço após o título

    # Prepara os dados da tabela
    data = [['Sócio', 'Tipo', 'Ano', 'Meses Pagos']]  # Cabeçalho da tabela

    for socio, mensalidades_socio in socios_com_mensalidades.items():
        # Adiciona a primeira linha com o nome, tipo e primeiro ano
        primeiro_ano = mensalidades_socio.first()
        if primeiro_ano:
            meses_pagos = primeiro_ano.get_meses_pagos()
            data.append([
                socio.nome,  # Nome do sócio
                socio.get_tipo_socio_display(),  # Tipo de sócio
                primeiro_ano.ano,  # Ano da mensalidade
                ', '.join(meses_pagos) if meses_pagos else ''  # Meses pagos
            ])

        # Adiciona os anos subsequentes (nome e tipo em branco)
        for mensalidade in mensalidades_socio[1:]:
            meses_pagos = mensalidade.get_meses_pagos()
            data.append([
                '',  # Nome em branco
                '',  # Tipo em branco
                mensalidade.ano,  # Ano da mensalidade
                ', '.join(meses_pagos) if meses_pagos else ''  # Meses pagos
            ])


    # Cria a tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho cinza
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto branco no cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centraliza todo o conteúdo
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte em negrito para o cabeçalho
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Espaçamento inferior para o cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fundo bege para as células de dados
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Adiciona bordas à tabela
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Alinha o nome à esquerda
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Alinha o tipo à esquerda
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Alinha o ano à esquerda
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),  # Alinha os meses pagos à esquerda
    ]))

    elements.append(table)

    # Gera o PDF
    doc.build(elements)
    return response


#-- views ===============================================================================
def grafico_mensalidades(request):
    dados = totalizar_mensalidades_por_ano()
    anos = [str(item['ano']) for item in dados]
    total_true = [item['total_true'] for item in dados]
    total_false = [item['total_false'] for item in dados]

    context = {
        'anos': json.dumps(anos, cls=DjangoJSONEncoder),
        'total_true': json.dumps(total_true, cls=DjangoJSONEncoder),
        'total_false': json.dumps(total_false, cls=DjangoJSONEncoder),
    }
    return render(request, 'relatorios/grafico_mensalidades.html',  context)

def grafico_tipos_socio(request):
    # Coletar todos os tipos de sócio
    tipos_socio = Socio.objects.values_list('tipo_socio', flat=True)
    
    # Contar a quantidade de cada tipo de sócio
    contagem_tipos_socio = Counter(tipos_socio)
    
    # Preparar os dados para o gráfico
    labels = list(contagem_tipos_socio.keys())
    data = list(contagem_tipos_socio.values())
    
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'relatorios/grafico_tipos_socio.html', context)
