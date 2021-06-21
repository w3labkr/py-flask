def main(template, **kwargs):
    if (template == 'kospi'):
        from .tmpl import kospi
        return kospi.main(**kwargs)
    elif (template == 'kosdaq'):
        from .tmpl import kosdaq
        return kosdaq.main(**kwargs)


if __name__ == '__main__':
    main()
