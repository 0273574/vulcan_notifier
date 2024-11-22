class NotificationManager:
    async def process_grades(self, grades, email_sender):
        for grade in grades:
            subject = f"Nowa ocena: {grade['subject']}"
            message = f"Otrzymałeś nową ocenę:\n\n" \
                      f"Przedmiot: {grade['subject']}\n" \
                      f"Ocena: {grade['value']}\n" \
                      f"Waga: {grade.get('weight', 'Nieznana')}"
            await email_sender.send_notification(subject, message)

    async def process_comments(self, comments, email_sender):
        for comment in comments:
            subject = f"Nowa uwaga od {comment['teacher']}"
            message = f"Dodano nową uwagę:\n\n" \
                      f"Nauczyciel: {comment['teacher']}\n" \
                      f"Treść: {comment['content']}\n" \
                      f"Data: {comment['date']}"
            await email_sender.send_notification(subject, message)

    async def process_tests(self, tests, email_sender):
        for test in tests:
            subject = f"Nadchodzący sprawdzian: {test['subject']}"
            message = f"Uwaga na sprawdzian!\n\n" \
                      f"Przedmiot: {test['subject']}\n" \
                      f"Data: {test['date']}\n" \
                      f"Typ: {test.get('type', 'Nieznany')}"
            await email_sender.send_notification(subject, message)
