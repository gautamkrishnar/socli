# Generate formula
pip install python-brewer
pybrew \
    -n "Socli" \
    -d "Stack overflow command line client. Search and browse stack overflow without leaving the terminal" \
    -H https://github.com/gautamkrishnar/socli \
    -g https://github.com/gautamkrishnar/socli.git \
    -r https://github.com/gautamkrishnar/socli/archive/${TRAVIS_TAG}.tar.gz \
    socli \
    socli.rb
echo "Generated formula:"
echo "------------------------------------------------------------------------------------"
cat socli.rb
echo ""
echo "------------------------------------------------------------------------------------"
# Pushing to tap
git config --global user.email "gkr@tuta.io"
git config --global user.name "gkr-bot"
echo "Pulling repo..."
git clone https://${BREW_GH_TOKEN}@github.com/gautamkrishnar/homebrew-socli.git brewroot > /dev/null 2>&1
echo "Generating formula..."
cp -fv socli.rb brewroot/Formula
cd brewroot
git add --all
echo "Committing formula..."
git commit -m "Published ${TRAVIS_TAG}"
echo "Pushing formula..."
git push --quiet