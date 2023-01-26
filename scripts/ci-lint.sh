CHECK_FLAG="--check"
BASE_DIR=./
echo $BASE_DIR

python3 -m black $CHECK_FLAG --exclude migrations --line-length=88 $BASE_DIR
python3 -m isort $CHECK_FLAG --profile black --skip migrations $BASE_DIR
python3 -m flake8 --config $BASE_DIR/scripts/setup.cfg $BASE_DIR