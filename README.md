### VimGolf

- Being fast at vim, why?

  - Does it make you a better programmer?
  - no
  - Will you save so much time that it makes you live life this? (beach photo)
  - no
  - Will you become a scientist?
  - no

- There is a joy in mastery

- My name is ThePrimeagen

  - wearing a hoody
  - typing with passion
  - Using a crazy keyboard
  - But seriously, Engineer at Netflix, Partnered Streamer on Twitch

- I need to do a bit of a back story, how did I get started in Vim?

  - Likely almost everyone else has a similar story, it all started when I saw
    someone else use it.
  - I remember that first experience learning the "more advanced" movements of
    vim.

- So what is mastery?
  - Mastery: comprehensive knowledge or skill in a subject or accomplishment.
  - My Def: Combination of knowledge and application.
  - In a netflix show, shameless plug, Jiro dreams of sushi, 3 years

* Remember, I am a scientist, just not a very good one. So I had some hypthosiseses

  - hypoth. D is faster than C:
  - Reasoning: d motion is followed by i, o, or a which is a trigger to start typing.
  - But I needed a way to measure it...

* Explain Vim APM

  - How fast am I?
  - What is fast?
  - Explain the tool.
  - So I needed a base line, which actually turned out to be an interesting
    problem.
    - One thing I did was ask for peoples data, which ended up yielding over
      11k data points
    - Obvi problem is that those 11k are from 5 people, which means that I
      really have 5 points of data.
    - So I had to figure out a way to compare myself against myself.

* Basics of Testing and hypothesisisizings.

  - You need a control
    - This is what normally happens
  - An experiment.
    - You then measure the experiment against the control with as few
      variables as possible.
    - Silicon Valley calls this AB testing.
  - But I didn't have an A and a B experience, I just had one, vim.
  - So I compared all my inputs against "basic input" entering, i

* Review the results

  - define terms, insertion time vs total time vs stroke time.

  - At first I compared myself against myself.
    - i is my control.
    - d insertion time ~= i insertion time.
    - c insertion time ~= terrible
    - c stroke time ~= terrible
