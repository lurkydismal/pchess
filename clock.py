#!/usr/bin/python

FRAMEBUFFER=False	# WIP

import pygame
from sys import argv, exit
from random import choice
from time import sleep
from datetime import datetime

bgcolor = (10, 10, 10)
xgcolor = (255, 0, 192)
fgcolor = (159, 182, 205)
xpcolor = (255, 0, 0)
green = (0, 255, 0)
fontsize = 42
linespace = -0
dotlines = 12

try:
	timeout = argv[2]*1000
except IndexError:
	timeout = 5*60*1000
try:
	num_players = argv[1]
except IndexError:
	num_players = 3

class NextPlayer(Exception): pass
class GameOver(Exception): pass

players = {}
for p in range(num_players):
	n = input(f"Player {p} name: ")
	players[n if n else f"Player {p}"] = timeout

def display(players, playing, t, nextp):
	pos_x = screen.get_rect().centerx/2
	pos_y = screen.get_rect().centery

	i = 0
	for p in players.keys():
		if p == playing:
			text = font.render(
					f"{p}: {t/1000:.3f} [s]",
					True, fgcolor, bgcolor
				)
		else:
			if p == nextp:
				text = font.render(
						">",
						True, xgcolor, bgcolor
					)
				screen.blit(text, (pos_x-fontsize/2, pos_y+((i)*(fontsize+linespace))) )
			text = font.render(
					f"{p}: {players[p]/1000:.3f} [s]{' '*3}",
					True, xgcolor, bgcolor
				)
		screen.blit(text, (pos_x, pos_y+((i)*(fontsize+linespace))) )
		i += 1



pygame.init()
if FRAMEBUFFER:
	os.putenv('SDL_FBDEV', '/dev/fb0')
	os.environ["SDL_VIDEODRIVER"] = 'fbcon'
	xmax = pygame.display.Info().current_w
	ymax = pygame.display.Info().current_h
	print("framebuffer size: %d x %d" % (self.xmax, self.ymax))
	screen = pygame.display.set_mode((xmax, ymax), pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode( (800,600) )
pygame.display.init()

#print(pygame.display.list_modes(  ))
pygame.display.set_caption('pchess clock')
screen.fill(bgcolor)

font = pygame.font.Font(None, fontsize)


try:
	running = False
	#now = int(perf_counter()*1000)
	now = int(datetime.now().timestamp()*1000)
	candidate = choice(list(players.keys()))
	nextp = None

	while True:
		try:
			r = (players[candidate]-(int(datetime.now().timestamp()*1000)-now))
			if r <= 0:
				print(f"{candidate} has run out of time!",end='\r')
				del(players[candidate])
				screen.fill(bgcolor)
				if len(players) == 1:
					raise GameOver
				else:
					raise NextPlayer
			#print(f"{candidate}: {r/1000:0.3f} [s]", end='\r')


			display( players, candidate, r, nextp )
			if not running:
				# TODO pausing doesn't really work... messes up the timing
				now = int(datetime.now().timestamp()*1000)

				text = font.render(
						"PAUSED",
						True, xpcolor, bgcolor
					)
				textRect = text.get_rect()
				textRect.centerx = screen.get_rect().centerx
				textRect.centery = screen.get_rect().centery
				screen.blit(text, textRect)
				#pygame.display.update()
			pygame.display.update()

			pygame.event.pump()
			keys = pygame.key.get_pressed()

			if keys[pygame.K_q]:
				exit()
			elif keys[pygame.K_ESCAPE]:
				running = not running
				sleep(.3)
				screen.fill(bgcolor)
			elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
				screen.fill(bgcolor)
				if not running:
					running = True
				else:
					raise NextPlayer
		except NextPlayer:
			P = players.copy()
			try:
				del P[candidate]
				players[candidate] = r
			except KeyError:
				pass
			now = int(datetime.now().timestamp()*1000)
			mx = max(P.values())
			candidates = [key for key, value in P.items() if value == mx]
			
			if len(candidates) != 1:
				candidate = choice(candidates)
			else:
				candidate = candidates[0]

			P = players.copy()
			del P[candidate]
			nextp = max(P, key=P.get)

			#print(f"{candidate}: {players[candidate]/1000:0.3f} [s]", end='\r')
			sleep(.3)
		except GameOver:
			print(f"\nGame over! the winner is {list(players.keys())[0]}")
			break


except KeyboardInterrupt:
	print(f"\nGame finished!")


