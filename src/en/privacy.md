title: Privacy Policy
description: How {{APP_NAME}} handles your data: personal budgets stay on your phone, group budgets are stored on our servers. What is stored, who sees it, how long it is kept and how to delete it.

# Privacy Policy

> Effective date: {{EFFECTIVE_DATE}}

{{APP_NAME}} (the "App") is an iPhone budget and expense tracker. It is operated by {{DEVELOPER_NAME}} ("we", "us"), who decides how and why your personal data is handled. This policy explains what the App handles, who receives it, how long it is kept, and what choices you have. Our contact details are in section 13.

## 1. The short version

- **No bank connection.** The App never asks for bank logins and does not connect to banks or card networks. You enter expenses yourself.
- **Personal channels stay on your phone.** A channel that is just for you is stored only on your iPhone. It is not sent to our servers, and the App has no iCloud sync.
- **Group channels are stored on our servers.** If you create or join a group, the group's data (names, expenses, balances, activity) is stored with Google Firebase in the United States, so that everyone in the group sees the same numbers. Only the members of the group can read it.
- **No sign-up.** There is no email, password or phone number. For groups, the App quietly creates an anonymous sign-in in the background. You can optionally connect it to your Apple Account so you can get your groups back on a new phone. We do not ask Apple for your name or email address.
- **No tracking, no ads, no analytics.** The App has no advertising or analytics software, does not track you across other companies' apps and websites, and we do not sell your data.
- **You can delete your group account in the App** (Profile > Delete group account).

## 2. Personal channels (on your phone only)

A personal ("Just me") channel, with its budget, transactions, categories, repeating rules and settings, is saved in the App's database on your iPhone. It is not uploaded to us or to anyone else, and we cannot see it. The App does not use iCloud syncing for it.

- **Device backups.** Like most apps, the App's data on your iPhone can be included in your device backup if you have iCloud Backup or a computer backup turned on. That backup is made and kept by Apple or by you under your own settings, not by us.
- **Recently deleted.** A personal transaction you delete stays on your phone in Recently deleted for 30 days, so you can bring it back. After that it is removed from the App's database.
- **Removing everything.** Deleting a channel removes it from the phone. Deleting the App removes the App's data from the phone (a restored backup can bring it back).
- **Other things on your phone.** Preferences, your optional profile name (shown on your home screen; it stays on this phone) and a small cache of exchange rates are also stored on the phone only.

## 3. Group channels (stored on our servers)

When you create a group, join one with an invite link or code, or are added to one, the App uses Google Firebase (Cloud Firestore, Cloud Functions, Authentication, Cloud Messaging, App Check and Hosting) as our backend. It runs in the United States (Iowa, region us-central1). A group belongs to no single person: it keeps existing even if the person who started it leaves.

| Information | What it is | Who can see it |
| --- | --- | --- |
| Anonymous sign-in ID | A random ID from Firebase Authentication, created in the background when you first create or join a group. It has no name, email or phone number. For members who have left, a one-way hash (a scrambled fingerprint) of the ID is kept, so that you get your old place back if you rejoin the same group. | Stored with your membership. Group members' apps receive it as part of the group record; we can see it. |
| Names | The display name you enter for the group (up to 40 characters), and names that members type for people who have not joined yet ("placeholders"). | Group members and us |
| Group details | Group name (up to 60 characters), main currency, optional end date, when it was created and by which member, and the member list with colors, join and leave times. | Group members and us |
| Expenses and settlements | For each expense: title (up to 80 characters), amount, currency and exchange rate used, category, date, who paid, who shares it and how much, and who created, edited or deleted it and when. For each settlement ("Settle up" record): who paid whom, amount and date. | Group members and us |
| Custom categories | Name, icon and color of categories the group added. | Group members and us |
| Activity history | A log written by our servers of what changed: who joined, left or was added, expenses and settlements added, edited, deleted or restored, group renamed, invite reset, categories added or renamed, plan changes. Entries carry a short summary (for example the expense title, amount and who paid). Members cannot edit the log. | Group members and us |
| Invite link and code | A random link token and a 10-character code. Our lookup records keep only a one-way hash of them. A readable copy is kept in the group's private invite record so that members can share it. Anyone who has the link or code can join (up to 10 people in total) until a member resets it. | Group members and us (the readable copy); hashes only for lookups |
| Abuse limits | Timestamps of recent wrong invite-code attempts for your sign-in ID (to stop guessing), and timestamps of recent notifications triggered by a member (to stop floods). | Us only |
| Notification registration | If you allow notifications: your Firebase Installation ID (an identifier for this install of the App), your sign-in ID, the platform (iOS), the language setting of your phone and the time of the last update. | Us only |
| Purchase verification | When a group is created or funded with a Group Plan purchase, your phone sends Apple's signed transaction to our server, which checks it. The group keeps a one-way hash of Apple's original transaction ID. A separate record, filed under that hash, keeps the product, whether it is a production or test purchase, the expiry, any refund or revocation time, and the ID and date of the last App Store notification. | Us only |

We do not store your name, email address, phone number, contacts, location, photos, bank or card details or your Apple Account details on our servers. Purchases are handled by Apple. We never see your payment card.

Expenses can be added without internet. They are kept in a cache on your phone and sent when you are back online.

## 4. Sign in with Apple (optional)

After you first use a group, the App may offer "Continue with Apple". It is optional and always available in Profile. If you use it, your anonymous sign-in is linked to your Apple identity so that your groups can be recovered on a new phone. The App asks Apple for no name and no email address; only Apple's identifier for your sign-in is connected to the account. Apple's own sign-in screens and privacy practices apply to what you share with Apple.

When you delete your group account and Apple is connected, the App asks you to confirm with Apple again and asks Apple to revoke the connection. If Apple cannot be reached, nothing is deleted and you can try again.

## 5. Notifications

Notifications are optional. The App asks for permission only once you have a group account, and only registers your device with our server if you allow them. When a member adds, edits, deletes or restores an expense or settlement, our server sends a short push notification to the other members it concerns. It contains the acting member's name, the expense title, the amount and the group name (for example "Ali added Dinner ($40.00) in Trip"). Notifications travel through Firebase Cloud Messaging and Apple's push notification service. They are written in English. You can turn them off in iOS Settings at any time; your device record then stops being useful and is removed automatically (section 7).

## 6. Who receives information

We share information only with the providers needed to run the App:

- **Google (Firebase and Google Cloud).** Hosting and processing of group data, the anonymous sign-in, notifications, App Check, and the static invite page. Google acts as our processor under its data processing terms. The invite page is a static web page on Firebase Hosting; it does not read or send the invite token, but, as with any web server, Google's infrastructure may process technical request data such as the IP address and the requested address (which contains the invite link) to deliver the page.
- **Apple.** App Store purchases and subscriptions (Apple handles payment and gives us signed transaction records and renewal or refund notices), push notifications, Sign in with Apple if you use it, and App Attest, which Firebase App Check uses to confirm that requests come from a genuine copy of the App. Apple is an independent party for its own services.
- **Frankfurter (exchange rates).** When you enter an amount in another currency, the App requests the day's exchange rate from the free Frankfurter service (api.frankfurter.dev, based on European Central Bank data). The request contains only currency codes, such as EUR and USD. No amount, name, group or account information is sent. As with any internet request, the service can see the IP address the request comes from. The rate is saved on your phone, and it is also saved with the transaction.
- **Other members of your group**, as described in section 3.
- **Authorities or successors**, when required by law or to protect rights and safety, or as part of a business transfer, with notice where the law requires it.

We do not sell your personal information and do not share it for advertising. The App contains no advertising, analytics or crash-reporting software.

## 7. How long we keep information

| Information | Retention |
| --- | --- |
| Personal channels | On your phone until you delete them or the App. A deleted personal transaction stays in Recently deleted for 30 days, then is removed. |
| Group expenses and settlements | As long as the group exists. When a member deletes one, it stays restorable for 30 days; a daily cleanup then permanently deletes it. The activity history keeps its short summary. |
| A group with no active members | If every member has left or deleted their account, the whole group (members, expenses, activity, invite records) is deleted after 30 days. If someone joins again through the invite link or code within that time, the deletion is cancelled. |
| Members, names, balances and the activity history of a group | As long as the group exists. A member who leaves loses access, but their name and balance stay in the group, so the other members' numbers stay correct. |
| Notification registrations | Refreshed whenever you open the App. Deleted when you delete your group account, when the push service reports the device as no longer valid (for example after you remove the App), and automatically when not refreshed for 60 days. |
| Invite-code attempt counters | Until you delete your group account. Notification limit counters are kept with the group. |
| Purchase verification records | They contain no name, account ID or payment details, and are kept as long as needed to keep groups funded and to process renewals and refunds. We have not set an automatic deletion date for them. |
| Technical logs | Google Cloud and Firebase keep technical logs (such as IP address, request time and error codes) for a limited period set by the platform. Our own code does not write expense details into them. |
| Backups | We do not keep separate backups of the group database. Deleted data is gone once the periods above end. If we turn on database backups in the future, we will update this policy first. |
| Support emails | As long as needed to help you, then deleted. |

## 8. Deleting your data and leaving groups

- **Leave a group.** You lose access to the group. Your name, your share of past expenses and your balance stay in the group, so that the other members' balances do not change. They can still record a settlement with you.
- **Delete group account** (Profile > Delete group account). You leave all your groups, and your name there is replaced by "Deleted member" (on your member record and in activity entries about you). Your notification registrations and code-attempt counter are deleted, and your anonymous sign-in is deleted from Firebase Authentication. If Apple is connected, the connection is revoked first. Expenses and settlements you entered, paid or shared stay in the group, with their titles, so the other members' balances stay correct. This cannot be undone. It does not cancel a subscription: manage that in your Apple Account settings. Your personal channels stay on your phone.
- **Delete a personal channel or transaction.** In the App. It never reached our servers.
- **Last member out.** When the last active member leaves or deletes their account, the group is deleted after 30 days (section 7).
- **By email.** If you cannot use the App (for example you lost your phone), write to us. Because the App has no login, we may need details such as the group name and the name you used in it, and we may not be able to find your record without them.

## 9. Your rights and choices

Depending on where you live, you may have the right to know what personal data we hold about you, to get a copy, to correct it, to delete it, to object to or restrict some processing, and to complain to a data protection authority. You can use the in-App tools in section 8 at any time. You can also email {{SUPPORT_EMAIL}} (see "By email" in section 8). We aim to answer within 30 days, or within the period the law that applies to you sets. We may ask you to confirm that a request concerns your own record. We will not treat you worse for using your rights.

- **United States.** Depending on your state, you may have rights to know, access, correct and delete your personal information and to appeal our decision. We do not sell personal information, do not share it for targeted advertising, and do not use it for profiling with legal or similarly significant effects. You may use an authorized agent. If we deny a request, you can appeal by replying to our email and you may contact your state attorney general.
- **Türkiye.** We are based in Türkiye. Under Article 11 of Law No. 6698 you may ask whether your data is processed, request information about it, ask for correction or deletion, and apply to us at the address in section 13. You may also complain to the Personal Data Protection Board.
- **Other countries.** If your local law gives you further rights over your personal data, we will honor them as far as they apply to us.
- **Permissions on your phone.** You can turn notifications off in iOS Settings at any time.

## 10. Children

The App is not directed to children, and we do not knowingly collect personal data from children under 13. Do not use the App if you are under 13. Where the law of your country sets a higher minimum age for consenting to the processing of personal data, you must be at least that age, or have the consent of a parent or guardian, to use the App. If you believe a child's data has been sent to us, contact {{SUPPORT_EMAIL}} and we will delete it.

## 11. International transfers and security

We are based in Türkiye, and our backend processes group data in the United States. If you live elsewhere, your group data is therefore transferred to the United States, where data protection law may differ from yours. We rely on the safeguards in our provider's data processing terms, and we send only the data the App needs.

Data moves between the App and our backend over encrypted connections (HTTPS/TLS), and Google encrypts stored data at rest. Security rules let only the members of a group read and write its data, and our servers verify purchases and write the activity log. Invite links and codes are stored in our lookup records only as hashes. No system is perfectly secure, so we cannot guarantee absolute security. If a breach affects your personal data, we will notify you and the authorities as the law requires.

## 12. Changes to this policy, and this website

If we change this policy in a meaningful way, we will update the effective date above and, if the change is significant, tell you in the App. If this policy is shown in a language other than English, the translation is provided for convenience and the English version prevails if the versions differ.

This website is static. It sets no cookies and uses no analytics or external resources. It is hosted on GitHub Pages, and GitHub may process technical data such as your IP address when your browser loads a page.

## 13. Contact

{{DEVELOPER_NAME}}
{{SUPPORT_EMAIL}}
{{SITE_URL}}/privacy.html
