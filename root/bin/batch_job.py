import MySQLdb
import sys
import os
from optparse     import OptionParser
import configparser
import logging
import csv
import datetime

root = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(root,"lib"))

connection = MySQLdb.connect(
	host='msadb.ch5vb2nmmcpb.us-west-2.rds.amazonaws.com',
	user='admin',
	passwd='password',
	db='msa_db',
	charset='utf8'
)
cursor = connection.cursor()

date = str('{0:%Y%m%d}'.format(datetime.datetime.now()))

def check_balance(wallet_id, master_balance, total_amount):
	if(wallet[2] == total_amount):
		logger.info("consistency success")
		logger.info("wallet_id=" + str(wallet_id))
		logger.info("master_balance=" + str(master_balance))
		logger.info("total_amount=" + str(total_amount))
	else:
		logger.error("consistency error")
		logger.error("wallet_id=" + str(wallet_id))
		logger.error("master_balance=" + str(master_balance))
		logger.error("total_amount=" + str(total_amount))


if __name__ == "__main__" :
	prog_name = os.path.splitext(os.path.basename(__file__))[0]

	usage = "usage: %prog (Argument-1) [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-d", "--debug",dest="debug", action="store_true", help="debug", default=False)
	(options, args) = parser.parse_args()

	# フォーマット
	log_format = logging.Formatter("%(asctime)s [%(levelname)8s] %(message)s")
	# レベル
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	# 標準出力へのハンドラ
	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setFormatter(log_format)
	logger.addHandler(stdout_handler)
	# ログファイルへのハンドラ
	file_handler = logging.FileHandler(os.path.join(root,"log", prog_name + ".log"), "a+")
	file_handler.setFormatter(log_format)
	logger.addHandler(file_handler)

	# 処理開始
	try:
		# ログ出力
		logger.info("job start - program : " + prog_name)

		wallet_list = []
		cursor.execute("select * from balance_wallet where wallet_id != 3 order by wallet_id asc")

		for wallet in cursor:
			wallet_list.append(list(wallet))

		with open("../file/wallet_list_" + date + ".csv", "w", encoding="Shift_jis") as f:
			writer = csv.writer(f, lineterminator="\n")
			writer.writerows(wallet_list)

		transaction_list = []
		cursor.execute("select * from balance_transaction order by wallet_id_id asc")

		for transaction in cursor:
			transaction_list.append(list(transaction))

		with open("../file/transaction_list" + date + ".csv", "w", encoding="Shift_jis") as f:
			writer = csv.writer(f, lineterminator="\n")
			writer.writerows(transaction_list)

		wallet_index = 0
		wallet_len = len(wallet_list)
		transaction_index = 0
		transaction_len = len(transaction_list)

		wallet =  wallet_list[wallet_index]
		transaction = transaction_list[transaction_index]
		total_amount = 0

		while wallet_index < wallet_len and transaction_index < transaction_len:
			wallet =  wallet_list[wallet_index]
			transaction = transaction_list[transaction_index]
			if(wallet[0] ==  transaction[6]):
				total_amount += transaction[2]
				transaction_index += 1
				if(transaction_index == transaction_len):
					check_balance(wallet[0], wallet[2], total_amount)
					break
			elif(wallet[0] <  transaction[6]):
				check_balance(wallet[0], wallet[2], total_amount)
				total_amount = 0
				wallet_index += 1
			else:
				break

		# オプション取得
		logger.info("job end - program : " + prog_name)
	except Exception as e:
		# キャッチして例外をログに記録
		logger.exception(e)
		sys.exit(1)