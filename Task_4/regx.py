import re
 
class RegxValidation : 
    def emailValidator(mail):
        val = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",mail)
        if val:
            print("Your email is valid")
        else:
            print("Email is not valid")
            
    def phoneValidator(number):
        phonevali = re.fullmatch(r"^(0|91)?[6-9][0-9]{9}$",number)
        if phonevali:
            print("Your Number is valid")
        else:
            print("Number is not valid")

    def textExtraction(string):
        emailmatch = re.findall(r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}',string)
        print("Email >> ", emailmatch)
        
        phonematch = re.findall(r'tel:?([6-9][0-9]{6,10})',string)
        print("Contact Numbers >> ", phonematch)
        
        datematch = re.findall(r'duedate:?([0-9]{1,2}[a-zA-Z]{3}[0-9]{4})',string)
        print("DueDate >> ",datematch)
        
        abnmatch = re.findall(r'[1-9][0-9]{10}',string)
        print("ABN Number >> ",abnmatch)
        
        invoicedate = re.findall(r'invoicedate:?([0-9]{1,2}[a-zA-Z]{3}[0-9]{4})',string)
        print("InvoiceDate >> ",invoicedate)
        
        amountdue = re.findall(r'amountdue:?([0-9]+\.[0-9]{2})',string)
        print("AmountDue >> ",amountdue)
    
        amountpaid = re.findall(r'amountpaid:?([0-9]+?\.[0-9]{2})',string)
        print("AmountDue >> ",amountpaid)

if __name__ == "__main__" :
    email = str(input("Enter Email ID >> "))
    RegxValidation.emailValidator(email)

    num = str(input("Enter Phone Number >> "))
    RegxValidation.phoneValidator(num)

    text = "paymentadviceto:allhourselectricalwaabn:54788190299tel:92752839email:service@allhourselectricalwa.com.aucustomertuvakhusidinvoicenumberinv-3649amountdue0.00duedate4jan2025amountenclosedentertheamountyouarepayingabovetaxinvoicetuvakhusidinvoicedate4jan2025invoicenumberinv-3649referencej2911abn54788190299allhourselectricalwaabn:54788190299tel:92752839email:service@allhourselectricalwa.com.audescriptionquantityunitpricegstamountaudinstalled1xclientsuppliedlight1.00150.0010%150.00job:j2911jobaddress:8salamanderstreet,dianellasubtotal150.00totalgst10%15.00totalaud165.00addcreditcardprocessingfee2.81lessamountpaid167.81amountdue0.00duedate:4jan2025pleaseusetheinvoicenumberasthepaymentreference.eftdetails:bsb066-167accno10617158paymenttermsstrictly:14daysifthereareanyqueriesaboutthisinvoice,pleasedonothesitatetocontactus.thankyouforusingus,weappreciateyourbusiness!"
    RegxValidation.textExtraction(text)
