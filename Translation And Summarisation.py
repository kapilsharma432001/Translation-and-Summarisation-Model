import requests
from tkinter import *
import tkinter as tk
from tkinter import filedialog
#Importing libraries for summarisation
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import docx2txt
from tkinter import messagebox
from googletrans import Translator, constants
from pprint import pprint


global punctuation
global text
global textBox
global textBox2
global textBox3
global textBox4



    
    

#Function for summarization
def abstractive_summarization(self,text):
    stopwords = list(STOP_WORDS)
    #Building nlp model
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text) #[Will tokenize the text]


    tokens = [token.text for token in doc]

    #Punctuations does not contain new line (\n), that's why adding new line to punctuation
    global punctuation
    punctuation += '\\n'
                 
    #Removing stop words and punctuation from text and counting word's frequency

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text]+=1


    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        try:
            word_frequencies[word] = word_frequencies[word]/max_frequency
        except:
            messagebox.showinfo("Info", "Text doesn't need summarisation!")
            

    #Performing sentence tokenization
    sentence_tokens = [sent for sent in doc.sents]


    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]



    sumValues = 0
    for sentence in sentence_scores: 
        sumValues += sentence_scores[sentence] 
               
    # Average value of a sentence from the original text 
    try:
        average = float(sumValues / len(sentence_scores))
    except:
        messagebox.showinfo("Info", "Text doesn't need summarisation!") 
              
    # Storing sentences into our summary.


    for sentence in sentence_scores:
        print(str(sentence)+' '+str(sentence_scores))
    summary = '' 
    for sentence in sentence_tokens: 
        if (sentence in sentence_scores)and (sentence_scores[sentence] >=(1.2 * average)): 
            summary += ''.join(str(sentence)) 
    print(summary) 



    print("Length of the original text = ",len(text))
    print("Length of the summary = ",len(summary))

    label = tk.Label(self,text = 'Length of the original text:',font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="780",y="554")
    label = tk.Label(self,text = 'Length of the summary:',font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="780",y="590")
    label = tk.Label(self,text =len(text),font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="1020",y="554")
    label = tk.Label(self,text =len(summary),font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="1000",y="590")
            


            
    label = tk.Label(self,text = 'Summary:-',font=('orbitron',15,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="860",y="160")
    textBox2=tk.Text(self, height=18, width=60,padx="2")
    textBox2.insert("1.0",summary)
    textBox2.place(x="1350",y="200",anchor="ne")


def summarization(self,text):

    if(len(text)<50):
        messagebox.showinfo("Info", "Text doesn't need summarisation!")

    url = "https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0"

    querystring = {"sentences":"5","txt":text}

    headers = {
        'accept': "application/json",
        'x-rapidapi-key': "d79a9f4502msh4b81175052de405jse12dc8b",
        'x-rapidapi-host': "meaningcloud-summarization-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response = response.json()


    summary = response["summary"]

    print("Length of the original text = ",len(text))
    print("Length of the summary = ",len(summary))

    label = tk.Label(self,text = 'Length of the original text:',font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="780",y="554")
    label = tk.Label(self,text = 'Length of the summary:',font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="780",y="590")
    label = tk.Label(self,text =len(text),font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="1020",y="554")
    label = tk.Label(self,text =len(summary),font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="1000",y="590")
            


            
    label = tk.Label(self,text = 'Summary:-',font=('orbitron',15,'bold'),foreground='white',background='#3d3d5c')
    label.place(x="860",y="160")
    textBox2=tk.Text(self, height=18, width=60,padx="2")
    textBox2.insert("1.0",summary)
    textBox2.place(x="1350",y="200",anchor="ne")

    def makeItSpeak():

        # Import the gTTS module for text  
        # to speech conversion  
        from gtts import gTTS

        import datetime

        # This module is imported so that we can  
        # play the converted audio  

        from playsound import playsound  

        # It is a text value that we want to convert to audio  
        text_val = summary  

        # English Language  
        language = 'en'

        # Passing the text and language to the engine,  
        # here we have assign slow=False. Which denotes  
        # the module that the transformed audio should  
        # have a high speed  
        obj = gTTS(text=text_val, lang=language, slow=False)  

        #Here we are saving the transformed audio in a mp3 file named  
        # exam.mp3

        date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = "voice"+date_string+".mp3"
        obj.save(filename)  

        # Play the exam.mp3 file  
        playsound(filename)  


        
        

    speakButton = tk.Button(self,text="LISTEN IT !",font = ('orbitron',10),fg='#3d3d5c',height=1,relief="raised",borderwidth=3,command=makeItSpeak,cursor="hand2")
    speakButton.place(x="1250",y="500")


    


#Function to upload the doc file
def uploadDocFile():
    docFile = filedialog.askopenfilenames(initialdir="/", title = "Select the PDF file for Summarization", filetypes = (("docx file","*.docx"), ("All files","*.*"),("doc file","*.doc")))
    print(docFile)
    docFile = str(docFile)
    docFile = docFile[2:-3]
    print(docFile)
    result = docx2txt.process(docFile)
    print(result)
    textBox.insert(tk.INSERT,result)
    

#Function to upload the pdf file
def uploadPdfFile():
    pdfFile = filedialog.askopenfilenames(initialdir="/", title = "Select the PDF file for Summarization", filetypes = (("pdf file","*.pdf"), ("All files","*.*")))
    print(pdfFile)
    pdfFile = str(pdfFile)
    pdfFile = pdfFile[2:-3]
    print(pdfFile)
    # importing required modules  
    import PyPDF2  
            
    # creating a pdf file object  
    pdfFileObj = open(str(pdfFile), 'rb')  
            
    # creating a pdf reader object  
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
            
    # printing number of pages in pdf file  
    print(pdfReader.numPages)  
            
    # creating a page object  
    pageObj = pdfReader.getPage(0)  
            
    # extracting text from page  
    print(pageObj.extractText())  
            
    # closing the pdf file object  
    pdfFileObj.close()  

       

def translateLanguages(self, text, lang1, lang2):

    langDict = {'english':'en', 'hindi':'hi', 'gujarati':'gu', 'tamil':'ta', 'urdu':'ur'}

    lang1 = lang1.lower()
    lang2 = lang2.lower()

    translator = Translator()

    translation = translator.translate(text, src = langDict[lang1],dest=langDict[lang2])
    

    textBox4=tk.Text(self, height=15, width=40,padx="2")
    textBox4.insert("1.0",translation.text)
    textBox4.place(x="1050",y="270",anchor="ne")


    def makeItSpeak():

        # Import the gTTS module for text  
        # to speech conversion  
        from gtts import gTTS

        import datetime

        # This module is imported so that we can  
        # play the converted audio  

        from playsound import playsound  

        # It is a text value that we want to convert to audio  
        text_val = translation.text  

        # Specifying language  
        language = langDict[lang2]

        # Passing the text and language to the engine,  
        # here we have assign slow=False. Which denotes  
        # the module that the transformed audio should  
        # have a high speed  
        obj = gTTS(text=text_val, lang=language, slow=False)  

        #Here we are saving the transformed audio in a mp3 file named  
        # exam.mp3

        date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = "voice"+date_string+".mp3"
        obj.save(filename)  

        # Play the exam.mp3 file  
        playsound(filename)  


        
        

    speakButton = tk.Button(self,text="MAKE IT SPEAK",font = ('orbitron',10),fg='#3d3d5c',height=1,relief="raised",borderwidth=3,command=makeItSpeak,cursor="hand2")
    speakButton.place(x="1080",y="270")


    

    
    


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

############ Class for home frame #############
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg = "#3d3d5c")
        self.controller = controller

        self.controller.title('Translation and Summarisation')
        self.controller.state('zoomed')
        self.controller.iconphoto(False,
                                  tk.PhotoImage(file = 'language.png'))
        headingLabel = tk.Label(self,text = 'Translation and Summarisation',font=('orbitron',45,'bold'),foreground='white',background='#3d3d5c')

        headingLabel.pack(pady=25)

        spaceLabel = tk.Label(self,height=4,bg='#3d3d5c')
        spaceLabel.pack()

        button1 = tk.Button(self, text="Click Here To Do Summarisation",relief='raised',borderwidth=3,width=40,height=3,font=('orbitron',10),fg='#3d3d5c',
                            command=lambda: controller.show_frame("PageOne"),cursor="hand2")
        button2 = tk.Button(self, text="Click Here To Do Translation",relief='raised',borderwidth=3,width=40,height=3,font=('orbitron',10),fg='#3d3d5c',
                            command=lambda: controller.show_frame("PageTwo"),cursor="hand2")
        button1.pack(pady=10)
        button2.pack()

########### Class for summarization frame ############
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg = "#3d3d5c")
        self.controller = controller
        label = tk.Label(self,text = 'Summarization',font=('orbitron',30,'bold'),foreground='white',background='#3d3d5c')
        label.pack()
        button = tk.Button(self, text="<--",relief='raised',borderwidth=3,width=4,height=1,font=('orbitron',10),fg='#3d3d5c',
                            command=lambda: controller.show_frame("StartPage"),cursor="hand2")
        button.pack(side="top",anchor="nw")
        





        uploadButton = tk.Button(self,text="UPLOAD",font = ('orbitron',10),fg='#3d3d5c',height=1,relief="raised",borderwidth=3,command=uploadDocFile,cursor="hand2")
        uploadButton.place(x="5",y="160")
        label = tk.Label(self,text = 'Enter your text here:-(Or upload a DOCX file using "UPLOAD" button)',font=('orbitron',15,'bold'),foreground='white',background='#3d3d5c')
        label.pack(anchor="nw",pady="40")
        
        def retrieve_input():
            text=textBox.get("1.0","end-1c")
            summarization(self,text)
        global textBox
        textBox=tk.Text(self, height=25, width=60,padx="2")
        textBox.pack(anchor="nw")
        summaryButton=tk.Button(self, text="Get The Summary",command=retrieve_input,relief='raised',cursor="hand2",borderwidth=3,width=15,height=1,font=('orbitron',10,'bold'),pady="10",fg='#3d3d5c')
        #command=lambda: retrieve_input() >>> just means do this when i press the button
        summaryButton.pack(anchor="nw")

############### Class for translation frame #################
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        options = [
        "English",
        "Hindi",
        "Urdu",
        "Tamil",
        "Gujarati"
        ]

        clicked1 = StringVar()
        clicked2 = StringVar()

        clicked1.set( "English" )
        clicked2.set( "Hindi" )


        def continueButtonClicked():
            label4 = tk.Label(self,text = 'Enter {} language sentences to translate into {}'.format(clicked1.get(), clicked2.get()),font=('orbitron',12,'bold'),foreground='white',background='#3d3d5c')
            label4.place(x="50",y="220")

            textBox3=tk.Text(self, height=15, width=40,padx="2")
            textBox3.place(x="50",y="270")


            def retrieve_input():
                text=textBox3.get("1.0","end-1c")
                translateLanguages(self,text,clicked1.get(),clicked2.get())
            
            translateButton=tk.Button(self, text="TRANSLATE",command=retrieve_input,relief='raised',cursor="hand2",borderwidth=3,width=14,height=1,font=('orbitron',10,'bold'),pady="10",fg='#3d3d5c')
            translateButton.place(x="500",y="295")
            

            

        
        tk.Frame.__init__(self, parent,bg = "#3d3d5c")
        self.controller = controller
        label = tk.Label(self,text = 'Translation',font=('orbitron',30,'bold'),foreground='white',background='#3d3d5c')
        label.pack()
        button = tk.Button(self, text="<--",relief='raised',borderwidth=3,width=4,height=1,font=('orbitron',10),fg='#3d3d5c',
                            command=lambda: controller.show_frame("StartPage"),cursor="hand2")
        button.pack(side="top",anchor="nw")


        label3 = tk.Label(self,text = 'CHOOSE THE LANGUAGES',font=('orbitron',15,'bold'),foreground='white',background='#3d3d5c')
        label3.place(x="50",y="80")
        
        label3 = tk.Label(self,text = 'TO',font=('orbitron',10,'bold'),foreground='white',background='#3d3d5c')
        label3.place(x="225",y="125")
        
        drop1 = tk.OptionMenu( self , clicked1 , *options)
        drop1.place(x="50",y="120")

        drop2 = tk.OptionMenu( self , clicked2 , *options)
        drop2.place(x="350",y="120")

        continueButton = tk.Button(self, text="CONTINUE",relief='raised',borderwidth=3,width=12,height=1,font=('orbitron',10),fg='#3d3d5c',
                            command=continueButtonClicked,cursor="hand2")
        continueButton.place(x="50",y="170")
        


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
