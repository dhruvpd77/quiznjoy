# QuizNjoy - Online Quiz Platform

A comprehensive Django-based quiz platform with Tailwind CSS frontend, designed for educational institutions to manage and conduct MCQ quizzes.

## 🚀 Features

### User Side
- **User Authentication**: Secure login and signup system
- **Semester/Subject/Unit Selection**: Hierarchical navigation through academic content
- **Two Quiz Modes**:
  - **Random Mode**: 10 random questions each time (may repeat)
  - **Practice All Mode**: Progressive practice with no repeats until all questions are covered
- **Quiz Taking**: Interactive MCQ interface with image support
- **Results & Review**: Detailed score display with correct answers
- **Profile & History**: Track all quiz attempts with performance metrics

### Admin Side
- **Semester Management**: Full CRUD operations for semesters
- **Subject Management**: Create and manage subjects within semesters
- **Question Management**: 
  - Manual question creation with image upload
  - Excel bulk upload with automatic image extraction
  - Unit-wise question organization
  - Bulk delete operations (by unit or by subject)
- **Excel Import**: 
  - Robust file reading with multiple fallback engines
  - Automatic image extraction from Excel cells
  - Code indentation preservation
  - Validation for complete MCQ questions (all 4 options required)

## 🛠️ Technology Stack

- **Backend**: Django 5.1.13
- **Frontend**: Tailwind CSS
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **Excel Processing**: pandas, openpyxl, xlrd
- **Image Processing**: Pillow

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhruvpd77/quiznjoy.git
   cd quiznjoy
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Local: http://127.0.0.1:8000
   - Network: http://YOUR_IP:8000 (configured for mobile access)

## 📱 Mobile Responsive

The entire platform is fully mobile responsive with:
- Hamburger menu navigation
- Touch-optimized buttons and inputs
- Responsive grid layouts
- Mobile-friendly forms and tables

## 📊 Excel Upload Format

Your Excel file should have the following columns:
- `unit_number`: The unit number for the question
- `question_text`: The question text (supports code with indentation)
- `option_a`, `option_b`, `option_c`, `option_d`: All four options (required)
- `correct_answer`: The correct answer (A, B, C, or D)
- Images: Embedded images in question cells will be automatically extracted

**Note**: Only questions with all 4 options filled will be imported.

## 🗂️ Project Structure

```
quiznjoy/
├── accounts/          # User authentication app
├── quiz/              # Quiz taking functionality
├── semesters/         # Semester, subject, question management
├── templates/         # HTML templates with Tailwind CSS
├── static/            # Static files (CSS, images, etc.)
├── media/             # User uploaded files (question images)
├── quiz_project/      # Django project settings
└── manage.py          # Django management script
```

## 🔐 Security Notes

- Change `SECRET_KEY` in `settings.py` for production
- Use environment variables for sensitive data
- Set `DEBUG = False` in production
- Configure proper `ALLOWED_HOSTS` for production
- Use a production database (PostgreSQL/MySQL)

## 📝 Admin Features

### Managing Questions
- View questions unit-wise
- Add questions manually with image upload
- Edit existing questions
- Delete individual questions
- Bulk delete by unit
- Bulk delete all questions in a subject

### Excel Upload
- Supports multiple Excel formats (.xlsx, .xls)
- Robust error handling for corrupted files
- Automatic image extraction
- Preserves code indentation

## 🐛 Troubleshooting

### Excel Upload Issues
If you encounter Excel file corruption errors:
1. Try the automated fix script: `python fix_excel_file.py "your_file.xlsx"`
2. Or manually: Open in Excel → Copy all → Paste into new workbook → Save
3. Or convert to CSV and back to Excel using `csv_to_excel.py`

See `EXCEL_TROUBLESHOOTING.md` for detailed solutions.

## 📄 License

This project is private and proprietary.

## 👤 Author

**Dhruv**
- GitHub: [@dhruvpd77](https://github.com/dhruvpd77)

## 🙏 Acknowledgments

- Django Framework
- Tailwind CSS
- Open source community

---

**Note**: This is a private repository. For access, contact the repository owner.
