from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 400), color='white')
d = ImageDraw.Draw(img)
d.text((100, 200), "Análisis de Sentimiento", fill="black")
img.save(r"C:")






def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets):
        fig = plt.figure()
        labels = ['Positivo [' + str(positive) + '%]', 'Ligeramente Positivo [' + str(wpositive) + '%]',
                'Fuertemente Positivo [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                'Negativo [' + str(negative) + '%]', 'Ligeramente Negativo [' + str(wnegative) + '%]',
                'Fuertemente Negativo [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        strFile = os.path.join(second.root_path, 'static', 'images', 'plot1.png')
        # Verifica si el archivo existe y elimínalo antes de guardar el nuevo
        if os.path.isfile(strFile):
            os.remove(strFile)
        plt.savefig(strFile)
        plt.close()
