import os 
import asposepdfcloud 
from asposepdfcloud.apis.pdf_api import PdfApi 
 
def updatePdf(inputFileName, srcTextArr, revisedTextArr):
    # Get App key and App SID from https://aspose.cloud 
    pdf_api_client = asposepdfcloud.api_client.ApiClient( 
        app_key='f2c07953a1fabe683f7b40dd162082b2', 
        app_sid='3eab99c4-c1b4-46ff-b715-9d4d68f40ba4') 
    
    pdf_api = PdfApi(pdf_api_client) 
    filename = inputFileName
    # print("This is input file name: " + inputFileName)
    # if (filename == inputFileName):
    #     print("Strings match")
    # else:
    #     print(filename, "\n", inputFileName)
    # TODO unique guid needs to be generated for each file name to handle multiple requests
    remote_name = 'revised_output.pdf' 
    # newSrcArr = []
    # newDestArry = []
    # newSrcArr.append('VASUKI')
    # newSrcArr.append('vasukidivya006@gmail.com')
    # newDestArry.append('SID')
    # newDestArry.append('smartsid2007@gmail.com')

        
    #upload PDF file to storage 
    pdf_api.upload_file(remote_name,filename) 
    text_replace_arr = []
    for i in range(len(srcTextArr)):
        #if(srcTextArr[i].strip() != ""):
        print(f"BeforeText is {srcTextArr[i]} and afterText is {revisedTextArr[i]}")
        text_replace_arr.append(asposepdfcloud.models.TextReplace(old_value=srcTextArr[i],new_value=revisedTextArr[i],regex='true')) 
        # print(f"BeforeText is {newSrcArr[i]} and afterText is {newDestArry[i]}")
        # text_replace_arr.append(asposepdfcloud.models.TextReplace(old_value=newSrcArr[i],new_value=newDestArry[i],regex='true')) 
    text_replace_model = asposepdfcloud.models.TextReplaceListRequest(text_replaces=text_replace_arr) 
    response = pdf_api.post_document_text_replace(remote_name, text_replace_model) 

    #Replace Text hard coded way
    # text_replace1 = asposepdfcloud.models.TextReplace(old_value='VASUKI',new_value='SID',regex='true') 
    # text_replace2 = asposepdfcloud.models.TextReplace(old_value='vasukidivya006@gmail.com',new_value='smartsid2007@gmail.com',regex='true') 
    # text_replace_list = asposepdfcloud.models.TextReplaceListRequest(text_replaces=[text_replace1,text_replace2])  
    # response = pdf_api.post_document_text_replace(remote_name, text_replace_list) 

    

    print(response)
    
    from shutil import copyfile 
    response_download = pdf_api.download_file(remote_name)
    copyfile(response_download, remote_name)
    return remote_name

