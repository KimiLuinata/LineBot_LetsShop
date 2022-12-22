from transitions.extensions import GraphMachine

from utils import *


class TocMachine(GraphMachine):
    budget = 0
    item = []
    unit = []
    price =[]
    total = []
    list = []
    total_price =0
    remain = 0
    curr = 0

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        reply_token = event.reply_token
        if text.lower() == 'fsm':
            send_image_message(event.reply_token, 'https://mail.google.com/mail/u/2?ui=2&ik=918d7096bf&attid=0.1&permmsgid=msg-f:1752933235927965202&th=1853ab7d9a765e12&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ-Z4CWLX8OfnT1Z2nZRRWFec-AIMTYUczltbVJ727Cq_AYPRWvWx0GKOjA7hqSBU4G7M1bzCElXLVc3peLiU39zWG5gL4WZEQ4d7ENesHo1P3mEiJVtKjIl8cU&disp=emb&realattid=ii_lbzbbq840')
        if(text.lower() != "start"):
            send_text_message(reply_token, "Hi! Let's plan your shopping list!\n"
                                "Please enter \"start\"!")
        return text.lower() == "start"

    def on_enter_start(self, event):
        print("I'm entering start")

        reply_token = event.reply_token
        send_text_message(reply_token, "Please enter your budget (ntd):")

    #get budget
    def is_going_to_addBudget(self, event):
        text = event.message.text
        if text.lower().isnumeric():
            money = int(text.lower())
            self.budget = money
            print(money)
        else:
            reply_token = event.reply_token
            send_text_message(reply_token, "Invalid!\n"
                                "Please re-enter your budget! (number)")
        return text.lower().isnumeric()

    def on_enter_addBudget(self, event):
        title = "Let's start!"
        text = "You can enter \"restart\" to restart making list!"
        btn = [
			MessageTemplateAction(
				label = "Add your first item!",
				text = "add"
			),
		]
        send_button_message(event.reply_token, title, text, btn)

    # add an item to list
    def is_going_to_addList(self, event):
        text = event.message.text
        return text.lower() == "add"   

    def is_going_to_addListAgain(self, event):
        text = event.message.text
        return text.lower() == "no" 

    def on_enter_addList(self, event):
        print("I'm entering addlist")

        reply_token = event.reply_token
        send_text_message(reply_token, "Please enter an item:")

    # choose delete an item 
    def is_going_to_delList(self, event):
        text = event.message.text
        return text.lower() == "del" 

    def on_enter_delList(self, event):
        num = 1
        reply = ("Here's your shopping list:\n")
        for i in self.list:
            reply += str(num) + ") " + i + "\n"
        reply += ("\nChoose the number of item you want to delete.")

        reply_token = event.reply_token
        send_text_message(reply_token, reply)

    # delete the item
    def is_going_to_delete(self, event):
        text = event.message.text
        if text.lower().isnumeric():
            idx = int(text.lower()) - 1
            if idx < self.curr:
                del self.item[idx]
                del self.unit[idx]
                del self.price[idx]
                del self.total[idx]
                del self.list[idx]
                self.curr -= 2

                num = 1
                reply = ("Here's your shopping list:\n")
                for i in self.list:
                    reply += str(num) + ") " + i + "\n"
                    num += 1
                reply += ("\nEnter \"menu\" to back to menu!")
                reply_token = event.reply_token
                send_text_message(reply_token, reply)
                return True

            else:
                reply_token = event.reply_token
                reply = ("Item not found!")
                send_text_message(reply_token, reply)
                return False

        else:
            reply_token = event.reply_token
            reply = ("Invalid!\n""Please re-enter the number!")
            send_text_message(reply_token, reply)
            return False

    # add the item price
    def is_going_to_addPrice(self, event):
        text = event.message.text
        if text.lower() == "restart":
            self.go_back()
        self.item.append(text.lower())
        return True 

    def on_enter_addPrice(self, event):
        print("I'm entering addPrice")

        reply_token = event.reply_token
        send_text_message(reply_token, "Please enter the item price:")

    # add the item unit
    def is_going_to_addUnit(self, event):
        text = event.message.text
        if text.lower().isnumeric():
            price = int(text.lower())
            self.price.append(price)

        else:
            reply_token = event.reply_token
            send_text_message(reply_token, "Invalid!\n"
                                "Please re-enter the Price! (number)")

        return text.lower().isnumeric()  

    def on_enter_addUnit(self, event):
        print("I'm entering addUnit")

        reply_token = event.reply_token
        send_text_message(reply_token, "Please enter the unit:")

    # confirm list
    def is_going_to_confirm(self, event):
        text = event.message.text
        if text.lower().isnumeric():
            unit = int(text.lower())
            self.unit.append(unit)

        else:
            reply_token = event.reply_token
            send_text_message(reply_token, "Invalid!\n"
                                "Please re-enter the unit! (number)")

        return text.lower().isnumeric()

    def on_enter_confirm(self, event):
        print(str(self.curr))
        if self.price:
            total = self.price[self.curr] * self.unit[self.curr]
            self.total.append(total)
            line = (self.item[self.curr] + " : " + str(self.unit[self.curr]) + " x " 
                    + str(self.price[self.curr]) + " ntd" + " = " + str(self.total[self.curr]) + " ntd")
            self.list.append(line)

        reply_token = event.reply_token
        send_text_message(reply_token, "Confirm your item? (\"yes\" / \"no\"):\n" + self.list[self.curr])

    # give menu
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "yes" or text.lower() == "menu"

    def on_enter_menu(self, event):
        print("I'm entering menu")

        self.curr += 1

        title = "Main Menu"
        text = "Let's plan your shopping list!"
        btn = [
			MessageTemplateAction(
				label = "Add another item",
				text = "add"
			),
			MessageTemplateAction(
				label = "Delete an item",
				text = "del"
			),
			MessageTemplateAction(
				label = "Show shopping list",
				text = "show list"
			),
            MessageTemplateAction(
				label = "Finish!",
				text = "finish"
			),
		]
        send_button_message(event.reply_token, title, text, btn)

    # check budget remains
    def is_going_to_checkBudget(self, event):
        text = event.message.text
        return text.lower() == "finish"

    def on_enter_checkBudget(self, event):
        for price in self.total:
            self.total_price += price
        self.remain = self.budget - self.total_price

        num = 1
        reply = ("Here's your shopping list:\n")
        for i in self.list:
            reply += str(num) + ") " + i + "\n"

        reply += "\nEnter \"check budget\" to check the remaining of your budget"

        reply_token = event.reply_token
        send_text_message(reply_token, reply)
        

    # budget remain positive
    def is_going_to_goodBudget(self, event):
        text = event.message.text
        if text.lower() == "check budget":
            return self.remain >= 0
        else:
            return False
    
    def on_enter_goodBudget(self, event):
        print("I'm entering goodBudget")

        reply_token = event.reply_token
        send_text_message(reply_token, "You spend: " + str(self.total_price) + " ntd.\n"
                                "With budget: " + str(self.budget) + " ntd."
                                "The rest of your budget is: " + str(self.remain) + " ntd.\n"
                                + "Enter \"finish\" to finish the list or \"menu\" to edit your list!")

    # budget remain negative
    def is_going_to_badBudget(self, event):
        text = event.message.text
        if text.lower() == "check budget":
            return self.remain < 0
        else:
            return False

    def on_enter_badBudget(self, event):
        print("I'm entering badBudget")

        reply_token = event.reply_token
        send_text_message(reply_token, "Your budget is not enough!\n "
                            "You spend: " + str(self.total_price) + " ntd.\n"
                            "With budget: " + str(self.budget) + " ntd."
                            "\n\nPlease return to menu to edit your list!")

    # show shopping list
    def is_going_to_showList(self, event):
        text = event.message.text
        return text.lower() == "show list"

    def on_enter_showList(self, event):
        num = 1
        reply = ("Here's your shopping list:\n")
        for i in self.list:
            reply += str(num) + ") " + i + "\n"

        reply += "\n Enter \"menu\" to back to menu!"
        reply_token = event.reply_token
        send_text_message(reply_token, reply)

    # final done
    def is_going_to_finalConfirm(self, event):
        num = 1
        reply = ("Thank you for making shopping list with me!"
                "Here's your shopping list:\n")
        for i in self.list:
            reply += str(num) + ") " + i + "\n"
        reply += ("\nTotal price = " + str(self.total_price) + "\n")
        reply += ("Budget = " + str(self.budget))

        reply += ("\nHappy Shopping!\n"
                "Do not buy things outside your list! :D\n")
        reply_token = event.reply_token
        send_text_message(reply_token, reply)
        self.go_back()