FROM php:8-apache

RUN a2enmod rewrite
RUN pecl install redis && docker-php-ext-enable redis
RUN apt update && apt install -y git

COPY --from=composer/composer /usr/bin/composer /usr/bin/composer
RUN cd /var/www/ && composer require vlucas/bulletphp

COPY ./flag/readflag.c /readflag.c
COPY ./flag/flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag
