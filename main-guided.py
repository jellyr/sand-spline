#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from copy import copy

from numpy import pi
from numpy import array
from numpy.random import randint
from numpy.random import random

from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import ones
from numpy import column_stack
from numpy import cos
from numpy import sin

from modules.helpers import _interpolate

TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 1500
PIX = 1.0/SIZE

GRID_X = 10
GRID_Y = 10
GNUM = 5

EDGE = 0.08
RAD = 0.5-EDGE
LEAP_X = (1.0-2*EDGE)/(GRID_X-1)*0.5*0.75
LEAP_Y = (1.0-2*EDGE)/(GRID_Y-1)*0.5*0.75

STEPS = 300
INUM = 2000


STP = 0.0005


GRAINS = 1


print('LEAP_Y', LEAP_Y)
print('LEAP_X', LEAP_X)
# print('STEPS', STEPS)
print('INUM', INUM)


def draw(render, xy):
  points = column_stack((xy[1:,:], xy[:-1,:]))
  render.sandstroke(points,GRAINS)

def f(x, y):
  while True:
    yield array([[x,y]])

def guides():
  res = []
  for x in linspace(EDGE, 1.0-EDGE, GRID_X):
    for y in linspace(EDGE, 1.0-EDGE, GRID_Y):
      res.append(f(x,y))
  return res

def spline_iterator():
  from modules.guidedSandSpline import GuidedSandSpline

  splines = []
  for guide in guides():

    pnum = 10
    a = random()*TWOPI + linspace(0, TWOPI, pnum)
    path = column_stack((cos(a), sin(a))) * LEAP_Y
    scale = arange(pnum).astype('float')*STP

    s = GuidedSandSpline(
        guide,
        path,
        INUM,
        scale
        )
    splines.append(s)

  itt = 0
  while True:
    for s in splines:
      xy = s.next()
      itt += 1
      yield itt, xy


def main():

  from render.render import Animate
  from fn import Fn


  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  def wrap(render):
    import sys, traceback
    try:
      itt, xy = si.next()
      draw(render, xy)
      if not itt%(GRID_Y*GRID_X):
        print(itt)
        render.write_to_png(fn.name())
      return True
    except StopIteration:
      render.write_to_png(fn.name())
      return False
    except Exception:
      render.write_to_png(fn.name())
      traceback.print_exc(file=sys.stdout)
      return False

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(PIX)
  render.transparent_pix()
  render.set_front(FRONT)

  render.start()


if __name__ == '__main__':
  main()

