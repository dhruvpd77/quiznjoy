# 📚 Unit Descriptions & PDF Syllabus Upload - Setup Guide

## ✅ What's Been Implemented

### 1. **Unit Model** (`semesters/models.py`)
- Stores unit information: title, description, topics
- Links to subjects
- Supports PDF syllabus upload
- Method to get topics as a list

### 2. **PDF Upload & Parsing** (`semesters/views.py`)
- `upload_syllabus_pdf()` - Upload PDF and extract units/topics
- `extract_text_from_pdf()` - Extract text from PDF (supports pdfplumber & PyPDF2)
- `parse_units_from_pdf()` - Smart parsing to extract:
  - Unit numbers (1-10, Roman numerals, etc.)
  - Unit titles
  - Topics (bullet points, numbered lists, etc.)

### 3. **Unit Management Views**
- `manage_units()` - View all units for a subject
- `edit_unit()` - Edit unit information manually
- `upload_syllabus_pdf()` - Upload and auto-extract from PDF

### 4. **Updated Quiz Views**
- `select_unit()` - Now shows unit descriptions and topics
- Enhanced unit display with titles, descriptions, and topic tags

### 5. **Dependencies Added**
- `PyPDF2==3.0.1` - PDF reading library
- `pdfplumber==0.10.3` - Better PDF text extraction

---

## 🚀 Next Steps to Complete

### Step 1: Create Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Install PDF Libraries
```bash
pip install PyPDF2 pdfplumber
```

### Step 3: Create Custom Template Filter
Create `quiz/templatetags/quiz_extras.py`:
```python
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary is None:
        return {}
    return dictionary.get(key, {})
```

Then in `templates/quiz/select_unit.html`, add at the top:
```django
{% load quiz_extras %}
```

### Step 4: Create Admin Templates
Create templates for:
- `semesters/upload_syllabus_pdf.html`
- `semesters/manage_units.html`
- `semesters/edit_unit.html`

### Step 5: Add Link in Admin Dashboard
Add link to "Manage Units" in subject management page

---

## 📋 How to Use

### For Admins:

1. **Upload Syllabus PDF:**
   - Go to: `/semesters/admin/upload-syllabus-pdf/<subject_id>/`
   - Upload PDF with unit-wise syllabus
   - System auto-extracts units and topics

2. **Manage Units:**
   - Go to: `/semesters/admin/manage-units/<subject_id>/`
   - View all units
   - Edit unit information manually
   - Add/update topics

3. **Edit Unit:**
   - Click "Edit" on any unit
   - Update title, description, topics
   - Topics can be comma-separated or newline-separated

### For Students:

- When selecting a unit, they'll see:
  - Unit title (if set)
  - Unit description
  - List of topics covered
  - Beautiful card layout with all info

---

## 🔍 PDF Parsing Patterns

The system recognizes:
- **Unit patterns:** "Unit 1", "UNIT 1", "Chapter 1", "1.", "1)", "1 -"
- **Topic patterns:** Bullet points (•, -, *), Numbered lists (1., 2.), Lettered lists (a., b.)
- **Roman numerals:** I, II, III, IV, V, VI, VII, VIII, IX, X

---

## 📝 Example PDF Format

```
Unit 1: Introduction to Programming
- Variables and Data Types
- Operators
- Control Structures

Unit 2: Functions and Modules
- Function Definition
- Parameters and Arguments
- Module Import
```

---

## 🎨 UI Features

- **Unit Cards:** Show unit number, title, description, and topics
- **Topic Tags:** Display first 3 topics, show "+X more" if more exist
- **Responsive Design:** Works on mobile and desktop
- **Hover Effects:** Beautiful animations on hover

---

## ⚠️ Important Notes

1. **PDF Quality:** Better formatted PDFs = better extraction
2. **Manual Editing:** You can always edit extracted data manually
3. **Unit Numbers:** Must match question unit numbers (1-10)
4. **Topics Format:** Can be comma or newline separated

---

## 🐛 Troubleshooting

**PDF not parsing correctly?**
- Check PDF text is selectable (not scanned image)
- Try manual editing in "Manage Units"
- Ensure unit numbers are clearly marked

**Units not showing?**
- Make sure units exist in Unit model
- Check unit numbers match question unit numbers
- Verify subject_id is correct

---

## 📦 Files Modified/Created

1. ✅ `semesters/models.py` - Added Unit model
2. ✅ `semesters/views.py` - Added PDF upload & parsing
3. ✅ `semesters/admin.py` - Registered Unit model
4. ✅ `semesters/urls.py` - Added new URLs
5. ✅ `quiz/views.py` - Updated select_unit view
6. ✅ `templates/quiz/select_unit.html` - Enhanced display
7. ✅ `requirements.txt` - Added PDF libraries

---

**Ready to use! Just run migrations and install dependencies!** 🚀

