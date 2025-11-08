# song2lrc

**A Python utility with a graphical interface that downloads lyrics from Musixmatch and generates simple `.lrc` files.**

**Based on the wrapper made by Strvm: [musicxmatch-api](https://github.com/Strvm/musicxmatch-api)**

---

## Overview

`song2lrc` allows the user to enter the song title in a user-friendly graphical window built with **CustomTkinter**. The program queries the public Musixmatch database, obtains the complete lyrics, and prompts the option to save them as a standard **LRC** file.

---

## Option 1:

Download the executable from the releases tab or by clicking [here](https://github.com/AngryPlayer04/song2lrc/releases).

## Option 2:

#### Requirements:

| Python | 3.12+  |
| ------ | ------ |
| Poetry | 2.2.1+ |

#### Clone the repository

```bash
git clone https://github.com/angryplayer04/song2lrc.git
cd song2lrc
```

#### Configure the environment with Poetry

Install Poetry if you don't already have it

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install the dependencies and create the virtual environment

```bash
poetry install
```

Poetry will create a dedicated virtual environment and install all necessary libraries (including customtkinter, requests, python-dotenv, etc.). 3️⃣ Activate the environment (optional)

```bash
poetry shell
```

### Run the program with:

```bash
poetry run python -m ui.ui
```

---

## Contributing

1. **Fork** the repository.
2. Create a descriptive branch (`git checkout -b my-feature`).
3. Implement the improvement or fix.
4. Update `pyproject.toml` if you need new dependencies (Poetry will handle the lock).
5. Open a **Pull Request** explaining the change.

## License

Distributed under the **MIT License** – see the [LICENSE](LICENSE) file for complete details.

---
