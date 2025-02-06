## 🤖 PepperART

This repository contains the project developed for the **"Human Robot Interaction" (HRI) and "Reasoning Agent" (RA)** courses at **La Sapienza University of Rome**, taught by **Prof. Luca Iocchi** and **Prof. Luca Patrizi**.

---

### 📌 Overview

The project focuses on **human-robot collaboration** to solve a **puzzle game** where a human user and a **Pepper robot** take turns swapping puzzle pieces. The goal is to **enhance interaction between humans and autonomous agents** while ensuring an optimal and engaging experience, since effective human-robot collaboration requires natural and rational interaction to ensure user comfort.

<p align="center">
  <img src="https://github.com/user-attachments/assets/37420790-cba5-4e98-9350-5adaf7401972" alt="schemaHri" width="300" height="auto">
</p>

This project aims to program a **humanoid robot** 🤖 to collaborate with users in solving puzzles representing **famous paintings from various periods of art history**. We chose to focus these puzzles on **art 🎨** because of its importance both as a means of personal expression.

Our robot, called **PepperART**, could be positioned inside an **art museum 🏛️**, engaging the public by proposing interactive puzzles. This aims to **increase fascination towards art for children** and provide adults with the chance to **learn interesting facts about the paintings**.

The puzzle is represented as a **picture of a painting divided into several pieces 🧩**, with both the number of pieces and the painting itself depending on the **difficulty level**. The goal is to **recreate the original image** using as **few moves as possible**. Each move involves **swapping two pieces** in their positions.

This is a **cooperative game 🎮**, where the **user makes a move**, followed by the **robot making a correct move**, and this sequence continues until the puzzle is solved.

The **puzzle difficulty** is suggested by **PepperART** after requesting some personal information about the user. They are free to follow this suggestion or decide the difficulty as they please. The difficulty level determines the **number of pieces** (9 or 16) and which **art masterpiece** is presented. The higher the level, the more complex the painting chosen. After solving the puzzle, the robot provides the user with a **simple explanation about the painting**, tailored to the user’s age.

During testing, we used the **Pepper SDK plugin in Android Studio 💻**, which provides an **emulator of the real robot**. Using the **QiSDK library** 📚, we implemented a series of **human-like movements** that the robot can perform, such as **greetings, animated arm movements during speech, dancing, etc.**

Regarding the **Reasoning Agent (RA)** part, we equipped the robot with the ability to **play the puzzle collaboratively** with the user, enabling it to reason about the puzzle and perform moves leading towards solving it. The **puzzle problem** was defined using **PDDL language** and solved via **various solvers** depending on the puzzle's difficulty. This allows **PepperART** to execute moves in the **shortest possible time**, making the interaction more fun and realistic. 🎯


### 🏗️ System Components

<p align="center">
  <img width="584" alt="schemaHri" src="https://github.com/user-attachments/assets/e233ed0b-d1cd-40a1-bed2-c14de96585ee" />
</p>

- **🖥️ Server & Game Logic** - The server manages game logic, optimizes moves using **PDDL-based planning**, and adapts to user performance.
- **📱 Android Application** - The Android app serves as Pepper's tablet interface, allowing users to interact with the puzzle and receive explanations.
- **🚀 Robot Control & Movement** - Pepper’s movements are executed via the **QiSDK library**, inside a **Docker** environment.

### 🎮 Features

- **🧩 Optimal Puzzle Solving**: The server computes the best sequence of moves for solving the puzzle in the fewest steps possible.
- **💡 Interactive Assistance**: If the user makes multiple errors, Pepper engages with them, offering help and guidance.
- **🔄 Turn-Based Gameplay**: Both the human and Pepper take turns swapping pieces, promoting collaborative problem-solving.
- **🎭 Human-Like Interaction**: The robot performs expressive gestures and uses natural language to enhance engagement.
- **🧠 AI-Powered Reasoning**: The game logic is implemented using **PDDL-based planning**, ensuring optimal puzzle-solving efficiency.

### ▶️ Watch the Simulation
https://github.com/user-attachments/assets/4bcc6cf4-ed8a-446b-a971-561184bab3d3

### 👥 Contributors

-  [Mattia Castelmare](https://github.com/MattiaCastelmare)
-  [Niccolò Piraino](https://github.com/Nickes10)
-  [Antonio Scardino](https://github.com/antoscardi)

---
