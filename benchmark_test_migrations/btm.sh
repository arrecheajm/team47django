if [ $# -eq 0 ]
    then
        echo 'Error: Correct usage is . btm monthday'
        exit 1
fi

#benchmarking using ApacheBench
ab -n 100 -c 10 https://33d2bef9-e4ad-48f3-9b55-d893e9b7764c-00-ft2ur0tp22md.worf.replit.dev/ > "$1_benchmark.txt"
cat "$1_benchmark.txt"
read -p "Press enter to continue.." -n1

cd ..
# echo '*********** Starting makemigrations...'
# python3 manage.py makemigrations > "benchmark_test_migrations/$1_migrations.txt"
# cat "benchmark_test_migrations/$1_migrations.txt"
# echo '*********** Finished makemigrations.'
# read -p "Press enter to continue.." -n1

echo '*********** Starting tests...'
python3 manage.py test &> "benchmark_test_migrations/$1_tests.txt"
cat "benchmark_test_migrations/$1_tests.txt"
echo '*********** Finished tests.'

cd -