## What is this about ?

Crawls news sources and extracts news


## Development & CI/CD

The project follows standard python project structure.

- The package and environment management is done by [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
- The tests are ```pytest``` tests.  Some tests are marked as slow, to run without the slow tests use ```pytest -m "not slow"```. Refer to ```pytest.ini```
- The configs are maintained by heroku style ``.env`` files. Python library [Dotenv](https://pypi.org/project/python-dotenv/) is used to read configs. 
- The ``env`` files contain sensitive/secret information so [git-secrets](https://git-secret.io/) is used. Make sure to follow the section on dealing with secrets
- The `./pre-commit` file creates makes sure to hide secrets before commit, use the `make`file to install the githook. 

### Secrets

[git-secrets](https://git-secret.io/) are used on the ``.env`` files. 

#### Quick installation notes:
- macos: 
`brew install git-secret`
- debian: 
```sh
echo "deb https://dl.bintray.com/sobolevn/deb git-secret main" | sudo tee -a /etc/apt/sources.list
wget -qO - https://api.bintray.com/users/sobolevn/keys/gpg/public.key | sudo apt-key add -
sudo apt-get update && sudo apt-get install git-secret
```
- Reference: [Installation manual](https://git-secret.io/installation)

#### Quick usage notes:
**Usage: Setting up git-secret in a repository**
These steps cover the basic process of using git-secret:

- Before starting, make sure you have created gpg RSA key-pair: public and secret key identified by your email address.

- Begin with an existing or new git repository. You’ll use the ‘`git secret’` commands to add the keyrings and information to make the git-secret hide and reveal files in this repository.

- Initialize the git-secret repository by running `git secret init` command. the `.gitsecret/` folder will be created, Note all the contents of the .gitsecret/ folder should be checked in, /except/ the random_seed file. In other words, of the files in .gitsecret, only the random_seed file should be mentioned in your .gitignore file.

- Add the first user to the git-secret repo keyring by running `git secret tell your@gpg.email`.

- Now it’s time to add files you wish to encrypt inside the git-secret repository. It can be done by running `git secret add <filenames...>` command. Make sure these files are ignored by mentions in `.gitignore`, otherwise git-secret won’t allow you to add them, as these files could be stored unencrypted.

- When done, run `git secret hide` to encrypt all files which you have added by the git secret add command. The data will be encrypted with the public-keys described by the git secret tell command. After using git secret hide to encrypt your data, it is safe to commit your changes. 
NOTE:. It’s recommended to add git secret hide command to your pre-commit hook, so you won’t miss any changes.

- Later you can decrypt files with the git secret reveal command, or just show their contents to stdout with the git secret cat command. If you used a password on your GPG key (always recommended), it will ask you for your password. And you’re done!

**Usage: Adding someone to a repository using git-secret**
Get their gpg public-key. You won’t need their secret key.

- Import this key into your gpg setup (in `~/.gnupg` or similar) by running `gpg --import KEY_NAME.txt`

Now add this person to your secrets repo by running git secret tell persons@email.id (this will be the email address associated with the public key)

The newly added user cannot yet read the encrypted files. Now, re-encrypt the files using `git secret reveal; git secret hide -d`, and then commit and push the newly encrypted files. (The -d options deletes the unencrypted file after re-encrypting it). Now the newly added user be able to decrypt the files in the repo using git-secret.

**Using gpg:**

You can follow a quick gpg [tutorial](https://www.devdungeon.com/content/gpg-tutorial). Here are the most useful commands to get started:

- To generate a RSA key-pair, run:
`gpg --gen-key`
- To export your public key, run:
`gpg --export your.email@address.com --armor > public-key.gpg`
- To import the public key of someone else (to share the secret with them for instance), run:
`gpg --import public-key.gpg`
- GPG folder default is `~/.gnupg`
- To see available GPG keys: `gpg --list-keys`
Be sure to use a secure channel to share your public key!

[Reference architecture](https://medium.com/vantageai/keeping-your-ml-model-in-shape-with-kafka-airflow-and-mlflow-143d20024ba6) 