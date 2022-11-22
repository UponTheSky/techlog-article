import { ArticlesController } from './articles/articles.controller';
import { MainController } from './main/main.controller';
import { MeController } from './me/me.controller';

const mainController = new MainController();
const meController = new MeController();
const articlesController = new ArticlesController();

export const controllers = [mainController, meController, articlesController];
