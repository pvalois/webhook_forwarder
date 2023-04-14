Ce role ansible déploie un script python qui extrait d'un envoie d'alertes openshift, la partie pertinente, et la tranfère sous forme text à un webhoot mattermost.

Paramétrage
============

Pour le jouer, créez les composants naturel d'ansible : 

```
├── inventories
│   └── hosts.yml
├── playbooks
│   └── webhooks.yml
└── roles
    └── webhook_forwarder
``` 

Clonez le repository dans roles
--------------------------------

```
cd roles
git clone https://github.com/pvalois/webhook_forwarder.git
```

Créer votre inventaire
-----------------------

Editez le fichier **inventory/hosts** comme suit : 

```
[all:children]
Prod
HorsProd

[Prod]
serveur1
serveur2

[HorsProd]
serveur3
serveur4
```

Créer le playbook
------------------

Editer le fichier **playbooks/webhooks_forwarder.yml** contenant : 

``` 
- name: Install Webhook forwarder for console
  hosts: 
    - all

  tasks:

    - name: import role
      include_role: 
        name: webhook_forwarder
``` 

Jouer le role  
--------------

```
ansible-playbook -i inventory/hosts playbooks/webhooks_forwarder.yml --ask-pass -K 
``` 
