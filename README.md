# edu-sharing to SKOS converter

This converter converts the edu-sharing topic collections developed by the Fachportalmanger:innen to SKOS vocabularies.

First install requirements: `pip install -r requirements.txt`.

## `convert-collection-to-skos.py`:
This will list all topics with their IDs.
You can then copy one and paste it in the command-line dialog.

## `auto-convert-collection-to-skos`:
This will take the `ids.json`-file and convert all collections mentioned there.
Below you find a list of currently available topics.
After every push a GitHub-Action is triggered.
It will checkout this repository, and build the vocabularies usind the `ids.json`-file in this repository.
After that it will get a skohub-vocabs container and publish the vocabulary using GitHub-Pages.

## Available Topics and their IDs

```json
{
  "Spanisch": "11bdb8a0-a9f5-4028-becc-cbf8e328dd4b",
  "Englisch": "15dbd166-fd31-4e01-aabd-524cfa4d2783",
  "Biologie": "15fce411-54d9-467f-8f35-61ea374a298d",
  "Türkisch": "26105802-9039-4add-bf21-07a0f89f6e70",
  "Informatik (alt!)": "2643cff3-80bf-4848-a132-19244ffe9c30",
  "Deutsch als Zweitsprache": "26a336bf-51c8-4b91-9a6c-f1cf67fd4ae4",
  "Geschichte": "324f24e3-6687-4e89-b8dd-2bd0e20ff733",
  "Chemie": "4940d5da-9b21-4ec0-8824-d16e0409e629",
  "Main-Collection (All)": "5e40e372-735c-4b17-bbf7-e827a5702b57",
  "Religion": "66c667bc-8777-4c57-b476-35f54ce9ff5d",
  "Deutsch": "69f9ff64-93da-4d68-b849-ebdf9fbdcc77",
  "Kunst": "6a3f5881-cce0-4e8d-b123-26392b3f1c19",
  "Informatik": "742d8c87-e5a3-4658-86f9-419c2cea6574",
  "Darstellendes Spiel": "7998f334-9311-491e-9a58-72baf2a7efd2",
  "Physik": "94f22c9b-0d3a-4c1c-8987-4c8e83f3a92e",
  "Open Educational Resources (OER)": "a87c092d-e3b5-43ef-81db-757ab1967646",
  "Mathematik": "bd8be6d5-0fbe-4534-a4b3-773154ba6abc",
  "Nachhaltigkeit": "d0ed50e6-a49f-4566-8f3b-c545cdf75067",
  "Sport": "ea776a48-b3f4-446c-b871-19f84b31d280",
  "Medienbildung": "eef047a3-58ba-419c-ab7d-3d0cfd04bb4e",
  "Politische Bildung": "ffd298b5-3a04-4d13-9d26-ddd5d3b5cedc"
}
```
