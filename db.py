import json

class Database:

    def insert(self,fname,lname,email,password):

        with open ( 'users.json', 'r') as rf:
            users = json.load(rf)

            if email in users:
                return 0
            else:
                users[email] = [fname,lname,password]

        with open ( 'users.json', 'w') as wf:
            json.dump(users,wf,indent=4)
            return 1

    def search(self, email, password):
        with open('users.json', 'r') as rf:
            users = json.load(rf)

            if email in users and users[email][2] == password:
                return {
                    "email": email,
                    "name": users[email][0] + " " + users[email][1]
                }
            else:
                return None
