from django.http import JsonResponse
from rest_framework.decorators import api_view

import PyPDF2
import docx
from odf import text, teletype
from odf.opendocument import load


from marking.marking_generator import generate_markings



@api_view(['GET'])
def ping(request):
    print('simply got pinged to trigger a start')

    return JsonResponse({})


@api_view(["POST"])
def marking(request):
    text = request.body.decode('utf-8')

    max_suggestions = int(request.GET.get('limit', '-1'))
    content = generate_markings(text, max_suggestions)

    return JsonResponse(content)


@api_view(["POST"])
def plagiarism(request):
    text = request.body.decode('utf-8')

    linksWithPercentages = {}

    # import pyink
    # linksWithPercentages = pyink.plagiarism.checkForPlagiarism(text)

    return JsonResponse(linksWithPercentages)


@api_view(["POST"])
def translation(request):
    text = request.body.decode('utf-8')

    textInEnglish = {}

    # import pyink
    # textInEnglish = pyink.translation.translateToEnglish(text)

    return JsonResponse(textInEnglish)

@api_view(["POST"])
def upload_document(request):
    print("POsth ke len")
    print(len(request.FILES))
    
    if len(request.FILES) != 1:
        
        raise ValueError('')

    uploaded_file_key = list(request.FILES.keys())[0]
    file = request.FILES[uploaded_file_key]
    print("file type o")
    print(file.content_type)
    
    microsoftFormat = docx.Document(file)
    
    fullText = []
    for para in microsoftFormat.paragraphs:
        fullText.append(para.text)

    text = ''
    if file.content_type == 'application/pdf':
        for page in PyPDF2.PdfFileReader(file.open()).pages:
            text += page.extractText()
    elif file.content_type == 'application/vnd.oasis.opendocument.text':
        pass  # .odt
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        for page in fullText:
            text += page
    elif file.content_type == 'application/msword':
        pass# .doc
    
    else:   
        raise ValueError('Document format not supported!')

    content = generate_markings(text)

    return JsonResponse(content)
