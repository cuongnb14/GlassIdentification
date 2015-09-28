#! /usr/bin/env python3
"""@author: cuongnb14 

"""
from statistics import *
import logging
import sys

logger = logging.getLogger("fs")

class Rule():
	"""Representation for a rule"""
	def __init__(self, condition, result, membership):
		"""init a rule

		@param list condition
		@param float result
		@param float membership 
		"""
		self.condition = condition
		self.result = result
		self.membership = membership

	def __repr__(self):
		condition = []
		for e in self.condition:
			condition.append("X"+str(e[0])+" is "+e[1]+str(e[0]))
		condition = " and ".join(condition)
		str_rule = "if " + condition + " then Y is "+str(self.result)+" ("+str(self.membership)+")"
		return str_rule


####### Function membership ##########

def get_membership_of_low(attr_index, value):
	"""Function membership of set Low

	Return membership of attribute in fuzzy set Low
	@param int attr_index, index of attribute
	@param float value of attribute 
	"""
	minv = attr_value[attr_index][0]
	maxv = attr_value[attr_index][1]
	membership = (value - minv)/(maxv-minv)
	return ((attr_index, 'L'), membership)

def get_membership_of_height(attr_index, value):
	"""Function membership of set Height

	Return membership of attribute in fuzzy set Height
	@param int attr_index, index of attribute
	@param float value of attribute 
	"""
	minv = attr_value[attr_index][0]
	maxv = attr_value[attr_index][1]
	membership = (value - maxv)/(minv-maxv)
	return ((attr_index, 'H'), membership)

def get_memberships (attr_index, value):
	"""Function memberships

	Return tuple (class, membership) of attribute
	@param int attr_index, index of attribute
	@param float value, value of attribute  
	@return list memberships, ((index_attr, class), membership)
	"""
	memberships = []
	memberships.append(get_membership_of_low(attr_index, value))
	memberships.append(get_membership_of_height(attr_index, value))
	return memberships


######## End Function membership #######
def generate_training_rule(data_line):
	"""Return Rule correspond with data_line
	
	@param string data_line, a line in data file
	@return Rule
	"""
	data_line = list(map(float, data_line.split(',')))
	condition = []
	min_membership = 1
	for i in range(len(data_line)):
		if(i == 0):
			continue
		if(i != 10):
			memberships = get_memberships(i, data_line[i])
			xi = max(memberships, key=lambda p: p[1])
			condition.append(xi[0])
			if(xi[1] < min_membership):
				min_membership = xi[1]
	rule = Rule(condition, data_line[10], min_membership)
	return rule

def append_rule(new_rule, rules):
	"""Append new rule in to traning rules
	
	@param Rule new_rule
	@param list rules	
	"""
	for i in range(len(rules)):
		if (rules[i].condition == new_rule.condition):
			if rules[i].membership < new_rule.membership:
				logger.info("delete rule: "+ str(rules[i]))
				del(rules[i])
				logger.info("append new rule: "+str(new_rule))
				rules.append(new_rule)
				return 0
	if(new_rule.membership > 0.5):
		logger.info("append new rule: "+str(new_rule))
		rules.append(new_rule)
	return 1

def is_up_therson(membership):
	if(membership[1] > 0.4):
		return True
	return False

def generate_test_rule(file_name):
	logger.info("start generate test rule")
	data = open(file_name)
	rules = []
	for data_line in data:
		condition = []
		data_line = list(map(float, data_line.split(',')))
		for i in range(len(data_line)):
			if(i == 0):
				continue
			if(i != 10):
				memberships = get_memberships(i, data_line[i])
				memberships = list(filter(is_up_therson, memberships))
				condition.append(memberships)
		conditions = [(x0,x1,x2,x3,x4,x5,x6,x7,x8) for x0 in condition[0] for x1 in condition[1] for x2 in condition[2] for x3 in condition[3] for x4 in condition[4] for x5 in condition[5] for x6 in condition[6] for x7 in condition[7] for x8 in condition[8] ]

		rule = (conditions, data_line[10])
		logger.info("append new rule: "+str(rule))	
		rules.append(rule)
	logger.info("finish generate test rule")
	data.close()
	return rules

def traning(file_name):
	"""Create set traning rules
	
	@param string path to file data
	@return list<Rule> 
	"""
	logger.info("start generate traning rule")
	data = open(file_name)
	rules = []
	for line in data:
		rule = generate_training_rule(line)	
		append_rule(rule, rules)
	logger.info("finish generate traning rule")
	data.close()
	return rules
	

def export_rule(file_name, rules):
	"""Export rules in @rules to file file_name 
	
	@param string file_name, path to file
	@param list rules
	"""
	logger.info("start export rules in to file: "+file_name)
	frules = open(file_name, "w")
	for rule in rules:
		logger.info("export rule: "+str(rule))
		frules.write(str(rule)+"\n")
	logger.info("finish export rule")
	frules.close()

def testing(traning_rules, test_rules):
	logger.info("start testing")
	total = len(test_rules)
	error = 0
	success = 0
	unknown = 0
	i = 0
	for test_rule in test_rules:
		rule_result = None
		max_membership = 0
		for condition in test_rule[0]:
			logger.info("test rule: "+str(test_rule))
			temp_con = [x[0] for x in condition]
			for traning_rule in traning_rules:
				if (temp_con == traning_rule.condition):
					membership_condition = min(condition, key=lambda p: p[1])
					membership_rule = membership_condition[1] * traning_rule.membership
					if(membership_rule > max_membership):
						max_membership = membership_rule
						rule_result = traning_rule
					break

		if(rule_result != None):
			if(test_rule[1] == rule_result.result):
				success += 1
			else:
				error += 1
		else:
			unknown += 1
		
	return {'total': total, 'error': error, 'success': success, 'unknown': unknown, 'accuracy': success*100/total}

def main():
	traning_rules = traning("data/glass.data")
	#export_rule("training_rule", traning_rules)
	test_rules = generate_test_rule("data/test.data")
	print(testing(traning_rules, test_rules))

if __name__ == "__main__":
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	logger.setLevel(logging.ERROR)
	main()
