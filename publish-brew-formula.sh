# Generate formula
pip install python-brewer
pybrew \
    -n "socli" \
    -d "Stack overflow command line client. Search and browse stack overflow without leaving the terminal" \
    -H https://github.com/gautamkrishnar/socli \
    -g https://github.com/gautamkrishnar/socli.git \
    -r https://github.com/gautamkrishnar/socli/archive/${TRAVIS_TAG}.tar.gz \
    socli \
    socli.rb
# Pushing to tap
git config --global user.email "gkr@tuta.io"
git config --global user.name "gkr-bot"
git clone https://${BREW_GH_TOKEN}@github.com/gautamkrishnar/homebrew-socli.git brewroot > /dev/null 2>&1
cp -fv socli.rb brewroot/Formula
cd brewroot
git add --all
git commit -m "Published ${TRAVIS_TAG}"
git push -f --quiet