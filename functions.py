import PyPDF2
import werkzeug.security


def hash_password(password):
    hashed_password = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    return hashed_password


def extract_text(pdf):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    pdf.close()
    return text


def user_exists(email, db, users):
    existing_user = db.session.query(users).filter_by(contact=email).first()
    if existing_user:
        return True
    else:
        return False




