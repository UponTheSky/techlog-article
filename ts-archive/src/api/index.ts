import { MainController } from './main/main.controller';
import { MeController } from './me/me.controller';
import { ArticlesController } from './articles/articles.controller';
import { AdminController } from './admin/admin.controller';

const mainController = new MainController();
const meController = new MeController();
const articlesController = new ArticlesController();
const adminController = new AdminController();

export const controllers = [
  mainController,
  meController,
  articlesController,
  adminController,
];
