import pathlib

import torch
from PIL import Image

from get_byteplot_image import *
from torchvision import transforms

<<<<<<< HEAD


=======

>>>>>>> ac6e4a2dd26ed6a1ff9d224b0ca01a6d33efeb66

#one merged model
labels_merged = []
#two models
labels = [True , False]
doc_labels = [False, True]

def convert_to_img(filepath):
    try:
        #data_transform = transforms.Compose(
        #    [transforms.Resize((256, 256)), transforms.ToTensor()])
        data_transform = transforms.Compose([transforms.ToTensor()])
        plot = get_byteplot_image(filepath)
        img = Image.fromarray(plot).convert('RGB')
        #img = img.resize((256,256))
        img = data_transform(img).unsqueeze(0)
        return img
    except:
        pass

def load_model():
    pathlib.WindowsPath = pathlib.PosixPath
    model = torch.load('cpu.pkl', map_location=torch.device('cpu'))
    model.eval()
    return model

def load_doc_model():
    pathlib.WindowsPath = pathlib.PosixPath
    model = torch.load('model_byteplot_doc_cpu.pkl', map_location=torch.device('cpu'))
    model.eval()
    return model

def load_merged_model():
    pathlib.WindowsPath = pathlib.PosixPath
    model = torch.load('cpu2.pkl', map_location=torch.device('cpu'))
    model.eval()
    return model
 
def predict(model, image):
    pred = model(image)
    return labels[pred.argmax()]

def predict_doc(model, image):
    pred = model(image)
    return doc_labels[pred.argmax()]



def main():
    #data_transform = transforms.Compose(
    #    [transforms.ToTensor()])
    #model = torch.load('cpu.pkl', map_location=torch.device('cpu'))
    #model.eval()
    #image = Image.open('2.png').convert('RGB')
    #image = data_transform(image).unsqueeze(0)
    #predict = model(image)
    #pred = predict.max(1, keepdim=True)[1]
    # print(pred)
    model = load_model()
    img = convert_to_img("notmalware")
    print(predict(model, img))


if __name__ == "__main__":
    main()
