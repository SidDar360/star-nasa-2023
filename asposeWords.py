import aspose.words as aw

def updatePdfLocally(inputFileName, srcTextArr, revisedTextArr):
    
    doc = aw.Document(inputFileName)
    builder = aw.DocumentBuilder(doc)

    # Insert text at the beginning of the document.
    builder.move_to_document_start()

    # doc.range.replace("MANN BELLANI", "SID DARAPURAM", aw.replacing.FindReplaceOptions(aw.replacing.FindReplaceDirection.FORWARD))

    for item in range(len(srcTextArr)):
        doc.range.replace(srcTextArr[item], revisedTextArr[item], aw.replacing.FindReplaceOptions(aw.replacing.FindReplaceDirection.FORWARD))

    # # Save the modified document
    # doc.save(ARTIFACTS_DIR + "FindAndReplace.simple_find_replace.docx")
    doc.update_page_layout()
    doc.save("/host-star/new-output.pdf")