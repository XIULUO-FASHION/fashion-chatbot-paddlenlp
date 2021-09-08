# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from markdownify import markdownify as md


from query import translate_query

def get_query(ls):
    ls_en = translate_query.get_trans_query(ls)
    str_en = 'generate: '+' '.join(ls_en)

    return str_en

def get_style(s):
    ls_en = translate_query.get_trans_query([s])
    str_en = 'styleSearch: '+' '.join(ls_en)
    
    return str_en

class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        dispatcher.utter_message(template="utter_first")
        # dispatcher.utter_message(md("您可以这样告诉我:<br/>\
        #                     我想要一条休闲裤<br/>\
        #                     酒会礼服<br/>\
        #                     我想设计牛仔夹克"))
        
        return [AllSlotsReset()]


class ActionDonKnow(Action):
    def name(self) -> Text:
        return "action_donknow"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message(template="utter_donknow")
        dispatcher.utter_message(md("您可以这样告诉我:<br/>\
                            我想要一条休闲裤<br/>\
                            酒会礼服<br/>\
                            我想设计牛仔夹克"))
        
        return [AllSlotsReset()]


class ActionRedesign(Action):
    def name(self) -> Text:
        return "action_redesign"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        dispatcher.utter_message(template="utter_redesign")
        dispatcher.utter_message(md("您可以这样告诉我:<br/>\
                            我想要一条休闲裤<br/>\
                            酒会礼服<br/>\
                            我想设计牛仔夹克"))
        
        return [AllSlotsReset()]


class ActionAskColor(Action):
    def name(self) -> Text:
        return "action_color"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        # category = tracker.get_slot("category")
        # print('action_color_print')
        dispatcher.utter_message(template="utter_color")

        return []

class ActionAskPattern(Action):
    def name(self) -> Text:
        return "action_pattern"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        category = tracker.get_slot("category")
        if category:
            if '裙' in category:
                dispatcher.utter_message(template="utter_pattern")
                return []    
            else:
                color = tracker.get_slot("color")
            
                search_ls = []
                if len(color) > 0:
                    search_ls.append(color)
                search_ls.append(category)
                query = get_query(search_ls)
            
                dispatcher.utter_message(md(query))
                dispatcher.utter_message(template="utter_wait")
                return [AllSlotsReset()]
        else:
            dispatcher.utter_message(template="utter_donknow")
            return [AllSlotsReset()]

class ActionAskSleeve(Action):
    def name(self) -> Text:
        return "action_sleeve"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        pattern = tracker.get_slot("pattern")
        if len(pattern) > 1:
            dispatcher.utter_message(template="utter_sleeve")
        else:
            dispatcher.utter_message(template="utter_wait")

        return []

class ActionSearch(Action):
    def name(self) -> Text:
        return "action_search"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        search_ls = []
        color = tracker.get_slot("color")
        pattern = tracker.get_slot("pattern")
        sleeve = tracker.get_slot("sleeve")
        category = tracker.get_slot("category")

        if category: # if slot is empty, object is type 'NoneType'. has no len()
            if len(color) > 0:
                search_ls.append(color)
            if len(pattern) > 0:
                search_ls.append(pattern)
            if len(sleeve) > 0:
                search_ls.append(sleeve)
            search_ls.append(category)

            query = get_query(search_ls)
            dispatcher.utter_message(md(query))
            dispatcher.utter_message(template="utter_wait")
        else:
            dispatcher.utter_message(template="utter_donknow")

        return [AllSlotsReset()]

class ActionStyle(Action):
    def name(self) -> Text:
        return "action_style"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        style = tracker.get_slot("style")

        if style: # if slot is empty, object is type 'NoneType'. has no len()
            query = get_style(style)
            dispatcher.utter_message(md(query))
            dispatcher.utter_message(template="utter_wait_style")
            dispatcher.utter_message(template="utter_color")
        else:
            dispatcher.utter_message(template="utter_donknow")  

        return []

