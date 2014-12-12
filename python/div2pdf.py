import pdfkit

def html2pdf(url):
    pdf=pdfkit.from_url(url,False)
    pdfkit.from_url(url,'x.pdf')

    
if __name__=="__main__":
    url='http://www.geeksforgeeks.org/snake-ladder-problem-2/'
    html2pdf(url)
    

