## OCIMAN 

A command line tool to automate ops over OCI Infrastructure

### Requirements
python >= 3.7

###Instructions

#### Install
```git clone https://github.com/davejfranco/ociman.git```

and 

```python setup.py install```

### How to use it

ociman uses the same config file format from the oci-cli something like 

```
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaai3vt3gh3otj74h776rgtzlcsbasjk7ywuboix4cn3tsvpq77s2ia
fingerprint=0d:fa:fd:8f:b4:b5:fb:b2:2e:i3:75:58:72:46:a0:e4
key_file=/Users/dave/.oci/oci-key.key.pem
tenancy=ocid1.tenancy.oc1..aaaaaaaax662yezpjh5nn3semo46qbt3enwcjd2w2a12fjsl6lkrbk2kxakq
region=us-ashburn-1
```

You can put it wherever you like and the default location is ~/.oci

### Some commands

- Get help
```ociman --help```

- List vms with a given freeform tag

```ociman --config config -l -t environment:dev --cid $cid```

- Soft stop vms with an specific tag

```ociman --config config --action softstop -t environment:dev --cid $cid```



