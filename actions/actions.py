import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

QUOTES = {
    "motivation": [
        "\"The secret of getting ahead is getting started.\" — Mark Twain",
        "\"It does not matter how slowly you go as long as you do not stop.\" — Confucius",
        "\"Our greatest glory is not in never falling, but in rising every time we fall.\" — Confucius",
        "\"Believe you can and you're halfway there.\" — Theodore Roosevelt",
        "\"You are never too old to set another goal or to dream a new dream.\" — C.S. Lewis",
        "\"The only way to do great work is to love what you do.\" — Steve Jobs",
        "\"Don't watch the clock; do what it does. Keep going.\" — Sam Levenson",
        "\"Act as if what you do makes a difference. It does.\" — William James",
        "\"Success is not final, failure is not fatal: It is the courage to continue that counts.\" — Winston Churchill",
        "\"Hardships often prepare ordinary people for an extraordinary destiny.\" — C.S. Lewis",
        "\"What you get by achieving your goals is not as important as what you become by achieving your goals.\" — Zig Ziglar",
        "\"You don't have to be great to start, but you have to start to be great.\" — Zig Ziglar",
        "\"The future belongs to those who believe in the beauty of their dreams.\" — Eleanor Roosevelt",
        "\"Start where you are. Use what you have. Do what you can.\" — Arthur Ashe",
        "\"Energy and persistence conquer all things.\" — Benjamin Franklin",
        "\"Strength does not come from physical capacity. It comes from an indomitable will.\" — Mahatma Gandhi",
        "\"Keep your eyes on the stars and your feet on the ground.\" — Theodore Roosevelt",
        "\"The only limit to our realization of tomorrow will be our doubts of today.\" — Franklin D. Roosevelt",
        "\"Do what you can, with what you have, where you are.\" — Theodore Roosevelt",
        "\"Push yourself, because no one else is going to do it for you.\"",
    ],
    "inspiration": [
        "\"The purpose of our lives is to be happy.\" — Dalai Lama",
        "\"Life is what happens when you're busy making other plans.\" — John Lennon",
        "\"Get busy living or get busy dying.\" — Stephen King",
        "\"You only live once, but if you do it right, once is enough.\" — Mae West",
        "\"Many of life's failures are people who did not realize how close they were to success when they gave up.\" — Thomas Edison",
        "\"If you want to live a happy life, tie it to a goal, not to people or things.\" — Albert Einstein",
        "\"Never let the fear of striking out keep you from playing the game.\" — Babe Ruth",
        "\"Money and success don't change people; they merely amplify what is already there.\" — Will Smith",
        "\"Your time is limited, don't waste it living someone else's life.\" — Steve Jobs",
        "\"Not how long, but how well you have lived is the main thing.\" — Seneca",
        "\"If life were predictable it would cease to be life, and be without flavor.\" — Eleanor Roosevelt",
        "\"In order to write about life first you must live it.\" — Ernest Hemingway",
        "\"The whole secret of a successful life is to find out what is one's destiny to do, and then do it.\" — Henry Ford",
        "\"To live is the rarest thing in the world. Most people exist, that is all.\" — Oscar Wilde",
        "\"Good things come to people who wait, but better things come to those who go out and get them.\"",
        "\"If you're not willing to risk the usual, you will have to settle for the ordinary.\" — Jim Rohn",
        "\"The big lesson in life is never be scared of anyone or anything.\" — Frank Sinatra",
        "\"Be yourself; everyone else is already taken.\" — Oscar Wilde",
        "\"Two roads diverged in a wood, and I took the one less traveled by, and that has made all the difference.\" — Robert Frost",
        "\"Imagination is more important than knowledge.\" — Albert Einstein",
    ],
    "love": [
        "\"The best thing to hold onto in life is each other.\" — Audrey Hepburn",
        "\"I have decided to stick with love. Hate is too great a burden to bear.\" — Martin Luther King Jr.",
        "\"Where there is love there is life.\" — Mahatma Gandhi",
        "\"The only thing we never get enough of is love; and the only thing we never give enough of is love.\" — Henry Miller",
        "\"You know you're in love when you can't fall asleep because reality is finally better than your dreams.\" — Dr. Seuss",
        "\"Love is composed of a single soul inhabiting two bodies.\" — Aristotle",
        "\"The best love is the kind that awakens the soul; that makes us reach for more, that plants a fire in our hearts.\" — Nicholas Sparks",
        "\"I love you without knowing how, or when, or from where. I love you simply, without problems or pride.\" — Pablo Neruda",
        "\"Love is not about how many days, months, or years you have been together. It's all about how much you love each other every day.\"",
        "\"To love and be loved is to feel the sun from both sides.\" — David Viscott",
        "\"You don't love someone for their looks or their clothes or their car. You love them because they sing a song only you can hear.\" — Oscar Wilde",
        "\"In all the world, there is no heart for me like yours. In all the world, there is no love for you like mine.\" — Maya Angelou",
        "\"Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.\" — Lao Tzu",
        "\"Love recognizes no barriers. It jumps hurdles, leaps fences, penetrates walls to arrive at its destination full of hope.\" — Maya Angelou",
        "\"The heart wants what it wants. There's no logic to these things.\" — Woody Allen",
        "\"If I know what love is, it is because of you.\" — Hermann Hesse",
        "\"We loved with a love that was more than love.\" — Edgar Allan Poe",
        "\"Love is an endless act of forgiveness. Forgiveness is the key to action and freedom.\" — Maya Angelou",
        "\"Whatever our souls are made of, his and mine are the same.\" — Emily Brontë",
        "\"To the world you may be one person, but to one person you may be the world.\" — Bill Wilson",
    ],
    "success": [
        "\"Success usually comes to those who are too busy to be looking for it.\" — Henry David Thoreau",
        "\"I find that the harder I work, the more luck I seem to have.\" — Thomas Jefferson",
        "\"The real test is not whether you avoid failure, because you won't. It's whether you let it harden or shame you into inaction, or whether you learn from it.\" — Barack Obama",
        "\"The only place where success comes before work is in the dictionary.\" — Vidal Sassoon",
        "\"If you really look closely, most overnight successes took a long time.\" — Steve Jobs",
        "\"The successful warrior is the average man, with laser-like focus.\" — Bruce Lee",
        "\"There are no secrets to success. It is the result of preparation, hard work, and learning from failure.\" — Colin Powell",
        "\"Success is walking from failure to failure with no loss of enthusiasm.\" — Winston Churchill",
        "\"If you are not willing to risk the usual, you will have to settle for the ordinary.\" — Jim Rohn",
        "\"Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.\" — Albert Schweitzer",
        "\"Don't aim for success if you want it; just do what you love and believe in, and it will come naturally.\" — David Frost",
        "\"Success is liking yourself, liking what you do, and liking how you do it.\" — Maya Angelou",
        "\"Opportunities don't happen. You create them.\" — Chris Grosser",
        "\"Try not to become a man of success. Rather become a man of value.\" — Albert Einstein",
        "\"Great minds discuss ideas; average minds discuss events; small minds discuss people.\" — Eleanor Roosevelt",
        "\"I have not failed. I've just found 10,000 ways that won't work.\" — Thomas Edison",
        "\"It's not whether you get knocked down, it's whether you get up.\" — Vince Lombardi",
        "\"If you genuinely want something, don't wait for it. Teach yourself to be impatient.\" — Gurbaksh Chahal",
        "\"The secret of success is to do the common thing uncommonly well.\" — John D. Rockefeller Jr.",
        "\"I never dreamed about success. I worked for it.\" — Estée Lauder",
    ],
    "funny": [
        "\"I am so clever that sometimes I don't understand a single word of what I am saying.\" — Oscar Wilde",
        "\"A day without sunshine is like, you know, night.\" — Steve Martin",
        "\"Before you criticize someone, walk a mile in their shoes. That way, you'll be a mile from them, and you'll have their shoes too.\" — Jack Handey",
        "\"The trouble with having an open mind, of course, is that people will insist on coming along and trying to put things in it.\" — Terry Pratchett",
        "\"Age is of no importance unless you're a cheese.\" — Billie Burke",
        "\"I used to think I was indecisive, but now I'm not so sure.\"",
        "\"Behind every great man is a woman rolling her eyes.\" — Jim Carrey",
        "\"The best way to teach your kids about taxes is by eating 30% of their ice cream.\" — Bill Murray",
        "\"I always wanted to be somebody, but now I realize I should have been more specific.\" — Lily Tomlin",
        "\"If you think you are too small to make a difference, try sleeping with a mosquito.\" — Dalai Lama",
        "\"People say nothing is impossible, but I do nothing every day.\" — A.A. Milne",
        "\"If at first you don't succeed, then skydiving definitely isn't for you.\" — Steven Wright",
        "\"The road to success is dotted with many tempting parking spaces.\" — Will Rogers",
        "\"I walk around like everything is fine, but deep down, inside my shoe, my sock is sliding off.\"",
        "\"Life is short. Smile while you still have teeth.\"",
        "\"Common sense is like deodorant. The people who need it most never use it.\"",
        "\"I'm not lazy. I'm on energy-saving mode.\"",
        "\"My bed is a magical place where I suddenly remember everything I forgot to do.\"",
        "\"I told my wife she was drawing her eyebrows too high. She looked surprised.\"",
        "\"I am not arguing. I am simply explaining why I am right.\"",
    ],
}


class ActionProvideMotivationQuote(Action):
    def name(self) -> Text:
        return "action_provide_motivation_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        quote = random.choice(QUOTES["motivation"])
        dispatcher.utter_message(text=quote)
        return [SlotSet("last_category", "motivation")]


class ActionProvideInspirationQuote(Action):
    def name(self) -> Text:
        return "action_provide_inspiration_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        quote = random.choice(QUOTES["inspiration"])
        dispatcher.utter_message(text=quote)
        return [SlotSet("last_category", "inspiration")]


class ActionProvideLoveQuote(Action):
    def name(self) -> Text:
        return "action_provide_love_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        quote = random.choice(QUOTES["love"])
        dispatcher.utter_message(text=quote)
        return [SlotSet("last_category", "love")]


class ActionProvideSuccessQuote(Action):
    def name(self) -> Text:
        return "action_provide_success_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        quote = random.choice(QUOTES["success"])
        dispatcher.utter_message(text=quote)
        return [SlotSet("last_category", "success")]


class ActionProvideFunnyQuote(Action):
    def name(self) -> Text:
        return "action_provide_funny_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        quote = random.choice(QUOTES["funny"])
        dispatcher.utter_message(text=quote)
        return [SlotSet("last_category", "funny")]
