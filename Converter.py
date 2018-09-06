import struct
import xlsxwriter


# Arabic character conversion goes here:
ar_charset = {  0xa5: 'ء',
                0xa6: 'آ',
                0xa7: 'أ',
                0xa8: 'ؤ',
                0xa9: 'إ',
                0xaa: 'ئ',
                0xab: 'ا',
                0xac: 'ب',
                0xad: 'ة',
                0xe0: 'ت',
                0xe1: 'ث',
                0xe2: 'ج',
                0xe3: 'ح',
                0xe4: 'خ',
                0xe5: 'د',
                0xe6: 'ذ',
                0xe7: 'ر',
                0xe8: 'ز',
                0xe9: 'س',
                0xea: 'ش',
                0xeb: 'ص',
                0xec: 'ض',
                0xed: 'ط',
                0xee: 'ظ',
                0xef: 'ع',
                0xf0: 'غ',
                0xf1: 'غ',
                0xf2: 'ف',
                0xf3: 'ق',
                0xf4: 'ك',
                0xf5: 'ل',
                0xf6: 'م',
                0xf8: 'ن',
                0xf9: 'ه',
                0xfb: 'و',
                0xfc: 'ى',
                0xfd: 'ي',
                0x20: ' '}

def get_string(characters_array):
    def ar(hex_val):
        try:
            return ar_charset[hex_val]
        except KeyError:
            return '?'
    string = [ar(c) if c > 0x7f else chr(c) for c in characters_array]
    return ''.join(string)

def get_db_info(data):
    records_count = struct.unpack('<I', data[4:8])[0]
    record_length = struct.unpack('<h', data[10:12])[0]
    first_record_pos = struct.unpack('<h', data[8:10])[0]
    return (records_count, first_record_pos, record_length)

def get_columns(data):
    first_record_location = get_db_info(data)[1]
    columns = []
    column_type = []
    columns_length = []
    # Taking a "line" every 32 bytes
    for b in range(32, first_record_location - 1):
        if b % 32 == 0:
            string = ''
            for byte in data[b:b+16]:
                if byte == 0:
                    break
                string += chr(byte)
            columns.append(string)
            column_type.append(chr(data[b+11]))
            columns_length.append(data[b+16])

    return (columns, columns_length, column_type)

def get_rows(data):
    rc, frl, rl = get_db_info(data)
    records_data = data[frl:]
    records = []
    rows = []

    for i in range(rc):
        r = [b for b in records_data[rl * i : rl * (i+1)]]
        records.append(r)

    for i in range(rc):
        records[i].remove(records[i][0])

    cols, col_len, col_type = get_columns(data)
    for i in range(rc):
        line = [None] * len(col_len)
        p = 0
        for j, n in enumerate(col_len):
            line[j] = get_string(records[i][p:p+n])
            p += n
        rows.append(line)

    return rows

def get_table(data):
    columns = get_columns(data)[0]
    rows = get_rows(data)
    return(columns, rows)

def get_subjects(class_num, data):
    sub_cols, sub_rows = get_table(data)
    classes_order = [int(r[0]) for r in sub_rows]
    number_of_subjects = [int(r[1]) for r in sub_rows]
    subjects = []

    for n, row in enumerate(sub_rows):
        c = 0
        class_sub = []
        for i, col in enumerate(sub_cols):
            if 'NAMES' in col:
                c += 1
                class_sub.append(row[i])
            if c >= number_of_subjects[n]:
                break
        subjects.append(class_sub)

    return subjects[classes_order.index(class_num)]

def get_classes_data(data):
    rows = get_rows(data)
    class_1 = [r for r in rows if int(r[0]) == 1]
    class_2 = [r for r in rows if int(r[0]) == 2]
    class_3 = [r for r in rows if int(r[0]) == 3]
    class_4 = [r for r in rows if int(r[0]) == 4]

    return (class_1, class_2, class_3, class_4)

def add_sheet(wb, class_data, subject_data):
    sub_count = len(subject_data)
    sheet = wb.add_worksheet(f'المرحلة {class_data[0][0]}')
    fmt = wb.add_format({'align': 'center', 'valign': 'vcenter',
                        'bg_color': 'black', 'fg_color': 'white',
                        'bold': True, 'border': 1})
    left_align = wb.add_format({'align': 'left'})
    marks_type = ['السعي', 'السعي السنوي النهائي 1', 'السعي السنوي النهائي 2',
                  'الدرجة النهائية د 1', 'الدرجة النهائية د 2']

    sheet.set_column('C:C', 30)

    # adding column header thing
    sheet.merge_range('A1:A2', 'رقم الطالب', fmt)
    sheet.merge_range('B1:B2', 'الشعبة', fmt)
    sheet.merge_range('C1:C2', 'الإسم', fmt)
    sheet.merge_range('D1:D2', 'الجنس', fmt)
    sheet.merge_range('E1:E2', 'الحالة', fmt)

    # adding subjects
    for i in range(sub_count):
        sheet.merge_range(0, 5*(i+1), 0, 5*(i+1)+4, subject_data[i], fmt)
        for j in range(len(marks_type)):
            sheet.write(1, 5*(i+1) + j, marks_type[j], fmt)

    move = sub_count + 1
    sheet.merge_range(0, 5*move + 1, 1, 5*move + 1, 'المعدل م1', fmt)
    sheet.merge_range(0, 5*move + 2, 1, 5*move + 2, 'المعدل م2', fmt)
    sheet.merge_range(0, 5*move + 3, 1, 5*move + 3, 'المعدل م3', fmt)
    sheet.merge_range(0, 5*move + 4, 1, 5*move + 4, 'المعدل م4', fmt)
    sheet.merge_range(0, 5*move + 5, 1, 5*move + 5, 'الجنسية', fmt)
    sheet.merge_range(0, 5*move + 6, 1, 5*move + 6, 'ملاحظات', fmt)

    # add class general data
    for i,r in enumerate(class_data):
        sheet.write(2+i, 0, int(r[2]))
        sheet.write(2+i, 1, r[1])
        sheet.write(2+i, 2, r[3])
        sheet.write(2+i, 5*move + 1, float(r[11]))
        sheet.write(2+i, 5*move + 2, float(r[12]))
        sheet.write(2+i, 5*move + 3, float(r[13]))
        sheet.write(2+i, 5*move + 4, float(r[14]))
        sheet.write(2+i, 5*move + 6, r[8], left_align)

        # sex
        if int(r[4]) == 1:
            sheet.write(2+i, 3, 'ذكر')
        elif int(r[4]) == 2:
            sheet.write(2+i, 3, 'أنثى')
        # status
        if int(r[6]) == 1:
            sheet.write(2+i, 4, 'مستمر')
        elif int(r[6]) == 2:
            sheet.write(2+i, 4, 'راسب')
        elif int(r[6]) == 3:
            sheet.write(2+i, 4, 'مؤجل')
        elif int(r[6]) == 4:
            sheet.write(2+i, 4, 'عسكري')
        # nationality
        if int(r[5]) == 1:
            sheet.write(2+i, 5*move + 5, 'عراقية')
        elif int(r[5]) == 2:
            sheet.write(2+i, 5*move + 5, r[-7])

    for i,r in enumerate(class_data):
        for c in range(sub_count):
            for m in range(len(marks_type)):
                move = 5 * (c+1) + m
                sheet.write(2+i, move, int(r[move+12]))

def convert(stud, sub, output):
    with open(stud, 'rb') as f:
        student_data = f.read()
    with open(sub, 'rb') as f:
        subject_data = f.read()

    s1 = get_subjects(1, subject_data)
    s2 = get_subjects(2, subject_data)
    s3 = get_subjects(3, subject_data)
    s4 = get_subjects(4, subject_data)
    c1, c2, c3, c4 = get_classes_data(student_data)

    workbook = xlsxwriter.Workbook(output)
    add_sheet(workbook, c1, s1)
    add_sheet(workbook, c2, s2)
    add_sheet(workbook, c3, s3)
    add_sheet(workbook, c4, s4)
    workbook.close()
