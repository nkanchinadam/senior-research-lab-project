from keras.models import load_model
import paths
import data_preparation as dp
import numpy as np

def max_prob(probs):
  max_prob = 0
  max_index = -1
  for i in range(len(probs)):
    if probs[i] > max_prob:
      max_prob = probs[i]
      max_index = i
  return max_index

def create_model_summary(model, x, y, labels):
  num_labels = len(labels) // 2
  classes = [[0 for j in range(num_labels)] for i in range(num_labels)]
  probs = model.predict(x, y)
  for i in range(len(probs)):
    max_index = max_prob(probs[i])
    classes[y[i]][max_index] += 1
  return classes

def main():
  to_load = input('Evaluate Abnormality Model: Input 0\nEvaluate Condition Model: Input 1\n')
  model_name = input('Model Name: ')

  labels = None
  model = None
  x_train = None
  y_train = None
  x_test = None
  y_test = None
  if to_load == '0':
    model = load_model(paths.ABNORMALITY_MODELS + model_name)
    labels = dp.get_labels(paths.ABNORMALITY_LABELS)
    x_train, y_train = dp.get_dataset(paths.ABNORMALITY_TRAIN, labels)
    x_test, y_test = dp.get_dataset(paths.ABNORMALITY_TEST, labels)
  elif to_load == '1':
    model = load_model(paths.CONDITION_MODELS + model_name)
    labels = dp.get_labels(paths.CONDITION_LABELS)
    x_train, y_train = dp.get_dataset(paths.CONDITION_TRAIN, labels)
    x_test, y_test = dp.get_dataset(paths.CONDITION_TEST, labels)

  train_classes = create_model_summary(model, x_train, y_train, labels)
  test_classes = create_model_summary(model, x_test, y_test, labels)

  print('Training Data')
  for i in range(len(train_classes)):
    print(labels[i])
    for j in range(len(train_classes[i])):
      print('\t' + labels[j] + ': ' + str(train_classes[i][j]))
  print()
  print('Testing Data')
  for i in range(len(test_classes)):
    print(labels[i])
    for j in range(len(test_classes[i])):
      print('\t' + labels[j] + ': ' + str(test_classes[i][j]))

if __name__ == "__main__":
  main()