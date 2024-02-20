# Baixar Mangás do Mangadex

Programa voltada para baixar mangás do Mangadex via Api

## Funcionalidades

Transforme o programa em executável, alterando manualmente o caminho para download

- [x] Baixar todos os capítulos publicados até do momento do mangá
- [x] Realizar a separação por volumes
- [x] Baixar volumes específicos
- [x] Baixar a capa de cada volume
- [x] Ver o status de algum mangá
- [x] Poder criar um lista de mangás que você ler semanalmente e ver se tem capítulos novos (Uso de redis ou Json)

### Como usar

Assim que transformar o programa em um executavel, usando o autopytoexe e adicionando como variavel de ambiente, o pŕograma funcionará da seguinte forma:

#### Baixar Mangá

mangadex "Nome do Mangá"

após a listagem dos capitulos, escolher o que baixar:

- Capítulos:

>10-30 -> Baixará os capitulos 10 ao 30

> todos -> Baixará todos os capitulos da listagem

- Volumes:
>volumes 1,4,5,10 -> Baixará os volumes 1,4,5,10
