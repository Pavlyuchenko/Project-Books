from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont  # Font
from reportlab.pdfbase import pdfmetrics  # Font
import math


all_lines_count = 0


def init_pdf(book):
    global all_lines_count
    all_lines_count = 0
    return canvas.Canvas(book.jmeno.replace(" ", "_") + '.pdf')


def init_fonts():
    # Register fonts
    pdfmetrics.registerFont(
        TTFont('Ubuntu_B', 'Ubuntu-Bold.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Ubuntu_M', 'Ubuntu-Medium.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Ubuntu_R', 'Ubuntu-Regular.ttf')
    )


def set_heading(pdf, book):
    pdf.setFont('Ubuntu_B', 38)
    pdf.setFillColorRGB(0.85098039215, 0.11764705882, 0.21176470588)
    pdf.drawCentredString(300, 780, book.jmeno)
    global all_lines_count


def set_author(pdf, book):
    pdf.setFont('Ubuntu_B', 18)
    pdf.setFillColorRGB(0.3294117647, 0.3294117647, 0.3294117647)
    pdf.drawCentredString(295, 755, book.author.jmeno)
    global all_lines_count


def write_line(pdf, text, x, y, color, font='Ubuntu_B', font_size=15):
    pdf.setFont(font, font_size)
    if color == 1: # Red
        r = 0.85098039215
        g = 0.11764705882
        b = 0.21176470588
        global all_lines_count
        all_lines_count += 2
    elif color == 2: # Grey
        r = g = b = 0.3294117647
    pdf.setFillColorRGB(r, g, b)
    pdf.drawString(x, y, text)


def main_postavy(book):
    postavy = ""
    postava_counter = 0
    for i in book.postavy:
        postavy += i.jmeno + ", "
        postava_counter += 1
        if postava_counter == 4:
            break
    return postavy[:-2]


def main_info(book):
    postavy = main_postavy(book)
    info = {}
    keys = ['Téma:', 'Motivy:', 'Časoprostor:', 'Datum dočtení:', 'Literární druh:', 'Literární žánr:', 'Hlavní postavy:',
            'Vypravěč:', 'Vyprávěcí způs.:', 'Typy promluv:']
    values = [book.hlavni_tema, book.motiv, book.casoprostor, str(book.datum_precteni.strftime('%d. %m. %Y')),
              book.literarni_druh, book.zanr_id.zanr, postavy, book.vypravec, book.vypraveci_zpusoby, book.typy_promluv]
    for i, j in zip(keys, values):
        info[i] = j

    return info


def write_main_info(pdf, book):
    texts = main_info(book)
    for i in range(len(texts.keys())):
        write_line(pdf, list(texts.keys())[i], 30, 710 - i * 35, 1)

    for i in range(len(texts.values())):
        write_line(pdf, list(texts.values())[i], 155, 710 - i * 35, 2, font="Ubuntu_M")


def long_text(pdf, book, fill_text, x, y, title_text, title_x, font='Ubuntu_M', font_size=12, text_wrap=55):
    global all_lines_count

    pdf.setFont(font, font_size)
    if all_lines_count > 50:
        y = 800 * math.floor(all_lines_count/50) - abs(y)
        print(y)
    text = pdf.beginText(x, y)

    write_line(pdf, title_text, title_x, y, 1)

    r = g = b = 0.3294117647
    pdf.setFillColorRGB(r, g, b)

    res = wrap_text(fill_text, text_wrap)
    lines_count = 0
    for line in res:
        lines_count += 1
        all_lines_count += math.sqrt(2)
        text.textLine(line)

        for i in range(100):
            if pdf.getPageNumber()-1 == i:
                max_lines = i*73 + 50
                break

        if math.ceil(all_lines_count) >= max_lines:
            pdf.drawText(text)
            new_page(pdf, book)
            pdf.setFont(font, font_size)
            pdf.setFillColorRGB(r, g, b)
            text = pdf.beginText(x, 800)
    pdf.drawText(text)

    return lines_count


def kompozice(book):
    kompo = book.kompozicni_vystavba
    if not kompo:
        kompo = book.kompozice
    return kompo


def footer(pdf, book):
    r = 0.85098039215
    g = 0.11764705882
    b = 0.21176470588
    pdf.setFillColorRGB(r, g, b)
    pdf.rect(0, 0, 800, 28, fill=True, stroke=False)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(12, 9, book.jmeno)
    pdf.drawCentredString(298, 9, str(pdf.getPageNumber()))

    x_pos = pdf.stringWidth(book.author.jmeno, 'Ubuntu_M', 15)
    pdf.drawString(580 - x_pos, 9, book.author.jmeno)


def new_page(pdf, book):
    footer(pdf, book)
    pdf.showPage()


def wrap_text(text, maximal_length):
    letter_counter = 0
    result = []
    curr_sentence = ""

    for i in text.split(" "):  # i is every word split by space in text

        if curr_sentence != "":
            curr_sentence += " "  # Add spaces between words

        word_letters_counter = 0
        for j in i:  # For each letter in word i
            if j == '&':
                curr_sentence += '\t'
            elif j == '<br />' or j == '<br>':
                curr_sentence += '\n'
            else:
                curr_sentence += j  # Add letter to sentence on current row
                word_letters_counter += 1
                letter_counter += 1  # Letter counter for line break

            if letter_counter >= maximal_length and len(i) >= 6 and (
                    word_letters_counter >= 4 and (len(i) - word_letters_counter) >= 3) and j not in [".", "-",
                                                                                                      ","]:  # If words have reached the end of row and word is longer than 6 letters
                curr_sentence += "-"  # Add hyphen for unfinished word
                result.append(str(curr_sentence))  # Add the whole sentence to the result
                curr_sentence = ""  # Reset current sentence
                letter_counter = 0  # Reset letter count

        if letter_counter >= maximal_length:  # If we reached end of row
            result.append(str(curr_sentence))  # Add the whole sentence to the result
            curr_sentence = ""  # Reset current sentence
            letter_counter = 0  # Reset letter count
    if not result:
        result.append(str(curr_sentence))
    elif result[-1] != curr_sentence:
        result.append(str(curr_sentence))
    if result[-1] == '':
        result = result[:-1]
    return result
