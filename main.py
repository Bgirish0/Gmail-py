def read(username, password, sender_of_interest=None):
    import email
    import imaplib
    # Login to INBOX
    
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login(username, password)
    imap.select('INBOX')
    # Use search(), not status()
    # Print all unread messages from a certain sender of interest
    if sender_of_interest:
        status, response = imap.uid('search', None, 'UNSEEN', 'FROM {0}'.format(sender_of_interest))
    else:
        status, response = imap.uid('search', None, 'UNSEEN')
    if status == 'OK':
        unread_msg_nums = response[0].split()
    else:
        unread_msg_nums = []
    data_list = []
    for e_id in unread_msg_nums:
        data_dict = {}
        e_id = e_id.decode('utf-8')
        _, response = imap.uid('fetch', e_id, '(RFC822)')
        html = response[0][1].decode('ISO-8859-1')
        email_message = email.message_from_string(html)
        data_dict['mail_to'] = email_message['To']
        data_dict['mail_subject'] = email_message['Subject']
        data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
        data_dict['body'] = email_message.get_payload()
        data_list.append(data_dict)
    print(data_list)
