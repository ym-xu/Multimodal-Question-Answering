
set -e
ROOT="./../open_domain_data"

while [ "$#" -gt 0 ]; do
    arg=$1
    case $1 in
        # convert "--opt=the value" to --opt "the value".
        # the quotes around the equals sign is to work around a
        # bug in emacs' syntax parsing
        --*'='*) shift; set -- "${arg%%=*}" "${arg#*=}" "$@"; continue;;
        -o|--output) shift; ROOT=$1;;
        -h|--help) usage; exit 0;;
        --) shift; break;;
        -*) usage_fatal "unknown option: '$1'";;
        *) break;; # reached the list of file names
    esac
    shift || usage_fatal "option '${arg}' requires a value"
done

DOWNLOAD=$ROOT/"download"

mkdir -p "${ROOT}"
mkdir -p "${DOWNLOAD}"
echo "Saving data in ""$ROOT"

# echo "Downloading Wikipedia passages"
# wget -c https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz -P "${DOWNLOAD}"
# echo "Decompressing Wikipedia passages"
# gzip -d "${DOWNLOAD}/psgs_w100.tsv.gz"
# mv "${DOWNLOAD}/psgs_w100.tsv" "${ROOT}/psgs_w100.tsv"

# wget -c https://raw.githubusercontent.com/google-research-datasets/natural-questions/master/nq_open/NQ-open.dev.jsonl -P "${DOWNLOAD}"
# wget -c https://raw.githubusercontent.com/google-research-datasets/natural-questions/master/nq_open/NQ-open.train.jsonl -P "${DOWNLOAD}"

# wget -c https://nlp.cs.princeton.edu/projects/entity-questions/dataset.zip -P "${DOWNLOAD}"
# unzip "${DOWNLOAD}/dataset.zip" -d "${DOWNLOAD}"

# wget -c https://dl.fbaipublicfiles.com/FiD/data/dataindex.tar.gz -P "${DOWNLOAD}"
# tar xvzf "${DOWNLOAD}/dataindex.tar.gz" -C "${DOWNLOAD}"
# wget -c https://dl.fbaipublicfiles.com/FiD/data/nq_passages.tar.gz -P "${DOWNLOAD}"
# tar xvzf "${DOWNLOAD}/nq_passages.tar.gz" -C "${DOWNLOAD}"

echo "Processing "$ROOT""
python src/preprocess.py $DOWNLOAD $ROOT
rm -r "${DOWNLOAD}"