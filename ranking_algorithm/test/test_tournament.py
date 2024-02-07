def test_tournament():
    from pandas import read_csv
    from main import main
    players = read_csv('test/animes.csv')['name']
    main(players)