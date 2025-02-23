# sre_cli

###      

Tested with

```shell
minikube version: v1.35.0
```

Create metrics server

```shell
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

#### Installation

Clone

```shell
git clone https://github.com/StasMiasnikov/sre_cli.git
```

```shell
cd sre_cli/src
```

```shell
pip install -r requirements.txt
```

Main help menu

```shell
python3 sre.py --help
```




