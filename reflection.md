# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
I will have 4 classes: Owner, Pets, Task and Scheduler. 

- What classes did you include, and what responsibilities did you assign to each?
Owner: it tell the owner what task they have to do for pets
Pets: what they need? Like walk, pet, eat, etc and they also store the information about the pets like breeds, weights, diet, etc.
Tasks: it will takes information from each pets, what they have to get for daily and show the onwer have to take care.
Scheduler: This will take from tasks and organize it base on how long does it takes, which one is more urgent, 

**b. Design changes**

- Did your design change during implementation?
yes, i did
- If yes, describe at least one change and why you made it.
I add the function to add pets in for the code, I want to see if an owner have 2 pets and if their schedule conflcits, how does the systems deal with that.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
I use duration and priority
- How did you decide which constraints mattered most?
I decide by the number of urgent (score), if it labels as high, the score is 60 score, medium is about 35 score and low is 15 so tasks have higher score will get to do first 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler prioritizes urgent tasks first, even if that means some lower-priority tasks are pushed out when daily time is limited.
- Why is that tradeoff reasonable for this scenario?
For pet care, missing a high-priority task (like medication or feeding) is more risky than delaying a low-priority task.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to brainstorm class design, improve method names, and connect my backend logic to the Streamlit UI. I also used it to debug edge cases like recurring tasks and conflict detection, and to clean up my README and test descriptions.
- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific ones, like asking for edge cases to test, asking how to update UML based on my final code, and asking how to use Scheduler methods directly in the app display logic.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment was when an AI suggestion included changes that were broader than what I needed for my assignment. I did not copy everything directly because I wanted to keep the project focused on the required features.
- How did you evaluate or verify what the AI suggested?
I checked whether each suggestion matched my actual class methods and project requirements, then verified behavior with my pytest tests (sorting, recurrence, and conflict warnings). If it did not match my code or scope, I revised it before using it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion, task addition storage, sorting by due time, building a daily plan in chronological order, filtering by completion and pet name, daily and weekly recurrence creation, time conflict detection, and conflict warning messages.
- Why were these tests important?
These tests were important because they cover the core scheduling flow and the highest-risk behaviors: ordering tasks correctly, handling recurring tasks automatically, and warning about overlapping times without crashing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am confident at about 8/10 for the implemented features because the main scheduling behaviors are covered by unit tests and manual UI checks.
- What edge cases would you test next if you had more time?
Next, I would test ties with the same due time across three or more tasks, recurrence across month/year boundaries, completing an already completed recurring task, and very tight daily time limits where only part of high-priority work can fit.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
After I fix everything and make sure every function, every details works, the localhost(Demo), I checked and played with everything works as intended, also make sure it gives me the warning rather than crash the systems.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
The Mermaid code for UML in the begining and the final is a whole different, the last one have mroe details, it makes more sense and easier to follow, each classes have their own functions and the relationship between them.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I think when design a systems like this, I always read what the AI gives me, I need to have the basic things in my head and how it works, then the AI gives me code, I take a look at it and mkae sure it do what I ask, I read line by line, also tests with multiple cases, make sure it works as intended, I play the game on website make sure there are no glitchs, things make sense. 
